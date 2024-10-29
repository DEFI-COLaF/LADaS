from dotenv.main import DotEnv
from roboflow import Roboflow
import yaml
import pathlib
from util import rel_path
import sys
import os

def download(force=False):
    with open(rel_path("status.yml")) as f:
        status = yaml.safe_load(f)

    REQ = {
        "COLAF": 31,
        "DATACATALOGUE": 12,
        "THEATRE17": 5
    }

    # raise Exception
    env = DotEnv(rel_path(".env"))

    # Download COLaF
    if force or REQ["COLAF"] != status["COLAF"]:
        rf = Roboflow(api_key=env.get("COLAF"))
        project = rf.workspace("colaftextes").project("segmonto")
        os.makedirs("data-colaf", exist_ok=True)
        dataset = project.version(REQ["COLAF"]).download("yolov8", location=rel_path("data-colaf"), overwrite=True)

    if force or REQ["DATACATALOGUE"] != status["DATACATALOGUE"]:
        rf = Roboflow(api_key=env.get("DATACATALOGUE"))
        project = rf.workspace("datacatalogue").project("macro-segmentation")
        os.makedirs("data-catalogue", exist_ok=True)
        dataset = project.version(REQ["DATACATALOGUE"]).download("yolov8", location=rel_path("data-catalogue"), overwrite=True)

    if force or REQ["THEATRE17"] != status["THEATRE17"]:
        rf = Roboflow(api_key=env.get("THEATRE17"))
        project = rf.workspace("theatreclassique").project("17e-siecle")
        os.makedirs("data-theatre-17e", exist_ok=True)
        dataset = project.version(REQ["THEATRE17"]).download("yolov8", location=rel_path("data-theatre-17e"), overwrite=True)


    with open(rel_path("status.yml"), "w") as f:
        yaml.dump(REQ, f)


if __name__ == "__main__":
    print(sys.argv)
    if "--force" in sys.argv:
        download(force=True)
    else:
        download()