import collections
import os.path
import shutil
from typing import Tuple, Dict

import yaml

from util import rel_path
import glob
import tqdm
import re

regex = re.compile(r"(_[a-z]+)$")


def rename(path: str) -> str:
    new = path.split(".rf.")[0]
    if "images/" in path:
        new = regex.sub(".jpg", new)
    else:
        new = regex.sub(".txt", new)

    if not new.endswith(".jpg") and "images/" in path:
        raise Exception(f"Missing _jpg in {path}")

    return new


def detect_subset(path) -> Tuple[str, bool]:
    """ Detect a subset folder

    :param path:
    :return: Tuple, first is the subset identifier, the second is a bool for reprocessing label map
    """
    bname = os.path.basename(path)
    if "data-colaf" in path:
        if bname.startswith("magazineJV"):
            return "magazine-tech", False
        elif bname.startswith("finger"):
            return "fingers", False
        elif re.match("^(bpt6|bd6t).*$", bname):
            return "monographies", False
        elif re.match("^these_.*$", bname):
            return "these", False
        elif re.match("^(PG).*$", bname):
            return "others", False
        elif re.match("^Tapuscrit.*$", bname):
            return "typewriter", False
        elif re.match("^Picard_Concours.*$", bname):
            return "picard", False
        elif re.match("^(20\d\d|19\d\d)[A-Z]{3,4}\d+_\d+.*$", bname):
            return "these", False
        else:
            return "persee", False
        return None
    elif "data-catalogue" in path:
        return "catalogue", True
    elif "data-theatre-17e" in path:
        return "theatre", True


def process(path: str = "data-*/*/images/*.jpg", maps: Dict[str, Dict[str, str]] = None):
    files = []
    counter = collections.Counter()
    maps = maps or {}
    for file in tqdm.tqdm(glob.glob(rel_path(path))):
        new_jpg = "/".join(rename(file).split("/")[-3:])
        txt = file.replace("images/", "labels/").replace(".jpg", ".txt")
        new_txt = "/".join(rename(txt).split("/")[-3:])
        subset, remap = detect_subset(file)
        counter[subset] += 1

        # JPG Processing
        tgt_jpg = rel_path(f"data/{subset}/{new_jpg}")
        os.makedirs(os.path.dirname(tgt_jpg), exist_ok=True)
        shutil.copy2(file, tgt_jpg)

        # Text Processing
        tgt_txt = rel_path(f"data/{subset}/{new_txt}")
        if remap:
            os.makedirs(os.path.dirname(tgt_txt), exist_ok=True)
            rewrite(txt, tgt_txt, maps=maps[subset])
        else:
            os.makedirs(os.path.dirname(tgt_txt), exist_ok=True)
            shutil.copy2(txt, tgt_txt)
    return files


def rewrite(source: str, target: str, maps: Dict[str, str]):
    data = []
    with open(source) as f:
        for line in f:
            idx, *pts = line.strip().split()
            data.append([maps[idx], *pts])
    with open(target, "w") as f:
        f.write("\n".join([
            " ".join(line)
            for line in data
        ]))


def parse_classes(folder: str) -> Tuple[str, ...]:
    with open(os.path.join(folder, "data.yaml")) as f:
        status = tuple(yaml.safe_load(f)["names"])
    return status


if __name__ == "__main__":
    OTHER_MAP = {
        'MainZone-CatalogueDesc': "MainZone-P",
        'MainZone-P-CatalogueDesc': "MainZone-P",
        "PageTitleZone": "TitlePageZone",
        "PageTitleZone-Index": "TitlePageZone-Index",
        "QuireMarkZone": "QuireMarksZone",
        "MainZone-Incipit": "MainZone-P",
        "MainZone-List": "MainZone-ListItem",
        # Merging Continued
        "MainZone-Entry-Continued": "MainZone-Continued",
        "MainZone-Lg-Continued": "MainZone-Continued",
        "MainZone-List-Continued": "MainZone-Continued",
        "MainZone-P-Continued": "MainZone-Continued",
        "MainZone-Sp-Continued": "MainZone-Continued",
        "MarginTextZone-Notes-Continued": "MarginTextZone-ContinuedNotes",
        # We stop merging TableZone
        "TableZone-Continued": "TableZone"
    }
    # COLAF has the biggest coverage, so we draw the classes from it
    # We now use a standardized Element in MAIN_MAP
    MAIN_MAP = parse_classes("./training-set")
    # Then we parse other maps
    YAML_MAP = {
        {
            "data-colaf": "COLAF", 
            "data-catalogue": "catalogue", 
            "data-theatre-17e": "theatre"
        }[os.path.basename(p)]: parse_classes(p)
        for p in glob.glob(rel_path("./data-*"))
    }

    for key, values in YAML_MAP.items():
        YAML_MAP[key] = {
            str(idx): str(
                MAIN_MAP.index(OTHER_MAP.get(cls, cls))
                if OTHER_MAP.get(cls, cls) in MAIN_MAP
                else (print(f"Missing zone translation for {cls}") or -1)
            )
            for idx, cls in enumerate(values)
        }

    process(maps=YAML_MAP)
