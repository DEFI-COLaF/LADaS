import collections
import os.path
import shutil
from typing import Tuple
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
        if bname.startswith("finger"):
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


def process(path: str = "data-*/*/images/*.jpg"):
    files = []
    counter = collections.Counter()
    for file in tqdm.tqdm(glob.glob(rel_path(path))):
        new_jpg = "/".join(rename(file).split("/")[-3:])
        txt = file.replace("images/", "labels/").replace(".jpg", ".txt")
        new_txt = "/".join(rename(txt).split("/")[-3:])
        subset, remap = detect_subset(file)
        counter[subset] += 1
        if remap:
            continue
        tgt_jpg = rel_path(f"data/{subset}/{new_jpg}")
        tgt_txt = rel_path(f"data/{subset}/{new_txt}")
        os.makedirs(os.path.dirname(tgt_jpg), exist_ok=True)
        os.makedirs(os.path.dirname(tgt_txt), exist_ok=True)
        shutil.copy2(file, tgt_jpg)
        shutil.copy2(txt, tgt_txt)
    return files


if __name__ == "__main__":
    shutil.copy2(rel_path("data-colaf/data.yaml"), rel_path("data/data.yaml"))

    process()
