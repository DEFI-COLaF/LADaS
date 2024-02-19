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
        else:
            return "persee", False
        return None
    elif "data-catalogue" in path:
        return "catalogue", True


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
        'MainZone-P-CatalogueDesc': "MainZone-P"
    }
    shutil.copy2(rel_path("data-colaf/data.yaml"), rel_path("data/data.yaml"))
    YAML_MAP = {
        {"data-colaf": "COLAF", "data-catalogue": "catalogue"}[os.path.basename(p)]: parse_classes(p)
        for p in glob.glob(rel_path("./data-*"))
    }
    for key, values in YAML_MAP.items():
        if key == "COLAF":
            continue
        YAML_MAP[key] = {
            str(idx): str(
                YAML_MAP["COLAF"].index(OTHER_MAP.get(cls, cls))
                if OTHER_MAP.get(cls, cls) in YAML_MAP["COLAF"]
                else -1
            )
            for idx, cls in enumerate(values)
        }

    process(maps=YAML_MAP)
