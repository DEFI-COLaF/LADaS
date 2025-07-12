import os
import zipfile
import yaml

from PIL import Image
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Tuple

ALTO_NS = "http://www.loc.gov/standards/alto/ns-v4#"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
SCHEMA_LOC = "http://www.loc.gov/standards/alto/ns-v4# https://gitlab.inria.fr/scripta/escriptorium/-/raw/develop/app/escriptorium/static/alto-4-1-baselines.xsd"


def load_class_names(yaml_path: str) -> dict:
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return {int(k): v for k, v in enumerate(data['names'])}



def create_tags_section(parent: ET.Element, class_names: Dict[int, str]):
    tags_elem = ET.SubElement(parent, "{http://www.loc.gov/standards/alto/ns-v4#}Tags")

    for class_id, label in sorted(class_names.items()):
        class_id = int(class_id)
        tag_id = f"BT{class_id}"
        description = f"block type {label}"
        ET.SubElement(tags_elem, "{http://www.loc.gov/standards/alto/ns-v4#}OtherTag", {
            "ID": tag_id,
            "LABEL": label,
            "DESCRIPTION": description
        })


def yolo_to_alto(yolo_file: Path, image_file: Path, class_names: Dict[int, str]) -> ET.ElementTree:
    # Image size
    with Image.open(image_file) as img:
        width, height = img.size

    ET.register_namespace('', ALTO_NS)
    ET.register_namespace('xsi', XSI_NS)

    # ALTO root with all required namespaces
    alto = ET.Element(f"{{{ALTO_NS}}}alto", {
        f"{{{XSI_NS}}}schemaLocation": SCHEMA_LOC
    })

    # Description section
    description = ET.SubElement(alto, f"{{{ALTO_NS}}}Description")
    ET.SubElement(description, f"{{{ALTO_NS}}}MeasurementUnit").text = "pixel"
    source_info = ET.SubElement(description, f"{{{ALTO_NS}}}sourceImageInformation")
    ET.SubElement(source_info, f"{{{ALTO_NS}}}fileName").text = image_file.name

    # Tags
    create_tags_section(alto, class_names)

    # Layout
    layout = ET.SubElement(alto, f"{{{ALTO_NS}}}Layout")
    page = ET.SubElement(layout, f"{{{ALTO_NS}}}Page", {
        "PHYSICAL_IMG_NR": "1",
        "ID": image_file.stem,
        "HEIGHT": str(height),
        "WIDTH": str(width),
    })

    print_space = ET.SubElement(page, f"{{{ALTO_NS}}}PrintSpace", {
        "HEIGHT": str(height),
        "WIDTH": str(width),
        "VPOS": "0",
        "HPOS": "0",
    })

    # Read YOLO annotations
    with open(yolo_file, 'r') as f:
        lines = f.read().splitlines()

    for i, line in enumerate(lines):
        cls_idx, xc, yc, w, h = map(float, line.strip().split())
        cls_idx = int(cls_idx)

        abs_x = int((xc - w / 2) * width)
        abs_y = int((yc - h / 2) * height)
        abs_w = int(w * width)
        abs_h = int(h * height)

        attrs = {
            "ID": f"e{i}",
            "HPOS": str(abs_x),
            "VPOS": str(abs_y),
            "WIDTH": str(abs_w),
            "HEIGHT": str(abs_h),
            "TAGREFS": f"BT{cls_idx}"
        }

        ET.SubElement(print_space, f"{{{ALTO_NS}}}TextBlock", attrs)

    return ET.ElementTree(alto)


def create_zip_from_yolo(yolo_dir: Path, output_zip: Path):
    images_dir = yolo_dir / "images"
    labels_dir = yolo_dir / "labels"
    yaml_path = yolo_dir / ".." / ".config.yaml"

    class_names = load_class_names(yaml_path)
    mets_entries = []

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for img_path in sorted(images_dir.glob("*.*")):
            label_path = labels_dir / (img_path.stem + ".txt")
            if not label_path.exists():
                continue

            # Add image
            zipf.write(img_path, arcname=img_path.name)

            # Generate ALTO XML
            alto_tree = yolo_to_alto(label_path, img_path, class_names)
            xml_filename = img_path.stem + ".xml"
            xml_bytes = ET.tostring(alto_tree.getroot(), encoding="utf-8", xml_declaration=True)

            # Add XML
            zipf.writestr(xml_filename, xml_bytes)
            mets_entries.append((img_path.name, xml_filename))

        # Write METS.xml
        mets_bytes = build_mets(mets_entries)
        zipf.writestr("mets.xml", mets_bytes)



def build_mets(images_and_xmls: List[Tuple[str, str]]) -> bytes:
    METS_NS = "http://www.loc.gov/METS/"
    XLINK_NS = "http://www.w3.org/1999/xlink"
    ET.register_namespace('', METS_NS)
    ET.register_namespace('xlink', XLINK_NS)

    mets = ET.Element(f"{{{METS_NS}}}mets")

    fileSec = ET.SubElement(mets, f"{{{METS_NS}}}fileSec")

    img_grp = ET.SubElement(fileSec, f"{{{METS_NS}}}fileGrp", USE="image")
    xml_grp = ET.SubElement(fileSec, f"{{{METS_NS}}}fileGrp", USE="export")

    structMap = ET.SubElement(mets, f"{{{METS_NS}}}structMap", TYPE="physical")
    doc_div = ET.SubElement(structMap, f"{{{METS_NS}}}div", TYPE="document")

    for i, (img, xml) in enumerate(images_and_xmls, start=1):
        image_id = f"image{i}"
        xml_id = f"export{i}"

        ET.SubElement(img_grp, f"{{{METS_NS}}}file", ID=image_id).append(
            ET.Element(f"{{{METS_NS}}}FLocat", {f"{{{XLINK_NS}}}href": img})
        )
        ET.SubElement(xml_grp, f"{{{METS_NS}}}file", ID=xml_id).append(
            ET.Element(f"{{{METS_NS}}}FLocat", {f"{{{XLINK_NS}}}href": xml})
        )

        page_div = ET.SubElement(doc_div, f"{{{METS_NS}}}div", TYPE="page")
        ET.SubElement(page_div, f"{{{METS_NS}}}fptr", FILEID=image_id)
        ET.SubElement(page_div, f"{{{METS_NS}}}fptr", FILEID=xml_id)

    return ET.tostring(mets, encoding="utf-8", xml_declaration=True)
# === USAGE ===
# Replace 'your/yolo/folder' with your actual YOLO dataset path
# The script creates 'output.zip' in the current working directory

if __name__ == "__main__":
    import glob
    for file in glob.glob("data/*/*"):
        if not os.path.isdir(file):
            continue

        yolo_folder = Path(file)
        output_zip = Path(file.replace("/", "-")+".zip")
        create_zip_from_yolo(yolo_folder, output_zip)
        print(f"Created zip: {output_zip}")
