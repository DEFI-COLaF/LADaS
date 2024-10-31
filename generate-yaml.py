import os
import glob
import yaml
from collections import defaultdict


results = defaultdict(dict)

with open("./training-set/data.yaml") as f:
    template_config = yaml.safe_load(f)

for subset in glob.glob("./data/*"):
    for s in ["train", "val", "test"]:
        template_config[s] = os.path.abspath(os.path.join(subset, s if s != "val" else "valid"))
    tempfile = ".config.yaml"
    
    with open(os.path.abspath(os.path.join(subset, tempfile)), "w") as f:
        yaml.dump(template_config, f)