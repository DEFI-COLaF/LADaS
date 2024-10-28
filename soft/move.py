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
            return "magazine-tech", "COLAF"
        elif bname.startswith("finger"):
            return "fingers", "COLAF"
        elif re.match("^(bpt6|bd6t).*$", bname):
            return "monographies", "COLAF"
        elif re.match("^these_.*$", bname):
            return "these", "COLAF"
        elif re.match("^(PG).*$", bname):
            return "others", "COLAF"
        elif re.match("^Tapuscrit.*$", bname):
            return "typewriter", "COLAF"
        elif re.match("^Picard_Concours.*$", bname):
            return "picard", "COLAF"
        elif re.match("^(20\d\d|19\d\d)[A-Z]{3,4}\d+_\d+.*$", bname):
            return "these", "COLAF"
        else:
            return "persee", "COLAF"
        return None
    elif "data-catalogue" in path:
        return "catalogue", "datacatalogue"
    elif "data-theatre-17e" in path:
        return "theatre", "theatre17"
    elif "data-ong" in path:
        return "administrative-report", "administrative-report"


def process(path: str = "data-*/*/images/*.jpg", maps: Dict[str, Dict[str, str]] = None):
    files = []
    counter = collections.Counter()
    maps = maps or {}
    for file in tqdm.tqdm(glob.glob(rel_path(path))):
        new_jpg = "/".join(rename(file).split("/")[-3:])
        txt = file.replace("images/", "labels/").replace(".jpg", ".txt")
        new_txt = "/".join(rename(txt).split("/")[-3:])
        subset, mapname = detect_subset(file)
        counter[subset] += 1

        # JPG Processing
        tgt_jpg = rel_path(f"data/{subset}/{new_jpg}")
        os.makedirs(os.path.dirname(tgt_jpg), exist_ok=True)
        shutil.copy2(file, tgt_jpg)

        # Text Processing
        tgt_txt = rel_path(f"data/{subset}/{new_txt}")
        os.makedirs(os.path.dirname(tgt_txt), exist_ok=True)
        rewrite(txt, tgt_txt, maps=maps[mapname])
    return files


def rewrite(source: str, target: str, maps: Dict[str, str]):
    data = []
    try:
        with open(source) as f:
            for line in f:
                idx, *pts = line.strip().split()
                data.append([maps[idx], *pts])
    except Exception as E:
        print(f"Error processing {source}")
        raise E
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
            "data-catalogue": "datacatalogue", 
            "data-theatre-17e": "theatre17",
            "data-ong": "administrative-report"
        }[os.path.basename(p)]: parse_classes(p)
        for p in glob.glob(rel_path("./data-*"))
    }

    # For every external set, we get the list of classes with their IDX
    for key, values in YAML_MAP.items():
        # For this YAML MAP
        YAML_MAP[key] = {}
        for idx, orig_cls in enumerate(values):
            mapped_id = -1
            cls = orig_cls
            # We check if it does not contain a forbidden char
            if ":" in cls or "#" in cls:
                cls = cls.replace(":", "-").replace("#", "-")

            # We first check its not in our values for global translations
            if cls in OTHER_MAP:
                cls = OTHER_MAP[cls]

            # Then, we look for the index of this label in the MAP of the training set
            if cls in MAIN_MAP:
                mapped_id = MAIN_MAP.index(cls)
                # We save this translation
                YAML_MAP[key][str(idx)] = str(mapped_id)
            else:
                print(f"Translation not found for `{orig_cls}` (=> `{cls}`)")

    process(maps=YAML_MAP)
