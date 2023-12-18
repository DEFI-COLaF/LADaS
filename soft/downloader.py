from dotenv.main import DotEnv
from roboflow import Roboflow
import yaml
import pathlib
from util import rel_path


def download():
    with open(rel_path("status.yml")) as f:
        status = yaml.safe_load(f)

    REQ = {
        "COLAF": 25,
        "DATACATALOGUE": 7
    }

    # raise Exception
    env = DotEnv(rel_path(".env"))

    # Download COLaF
    if REQ["COLAF"] != status["COLAF"]:
        rf = Roboflow(api_key=env.get("COLAF"))
        project = rf.workspace("colaftextes").project("segmonto")
        dataset = project.version(REQ["COLAF"]).download("yolov8", location=rel_path("data-colaf"))

    if REQ["DATACATALOGUE"] != status["DATACATALOGUE"]:
        rf = Roboflow(api_key=env.get("DATACATALOGUE"))
        project = rf.workspace("datacatalogue").project("macro-segmentation")
        dataset = project.version(REQ["DATACATALOGUE"]).download("yolov8", location=rel_path("data-catalogue"))

    with open(rel_path("status.yml"), "w") as f:
        yaml.dump(REQ, f)


if __name__ == "__main__":
    download()
