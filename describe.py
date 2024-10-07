import glob
import tabulate
import pandas as pd

data = {}

for dataset in glob.glob("./data/*"):
	ds_name = dataset.split("/")[-1]
	data[ds_name] = {}
	for split in glob.glob(f"{dataset}/*"):
		split_name = split.split("/")[-1]
		data[ds_name][split_name] = len(glob.glob(f"{split}/labels/*.txt"))

print(tabulate.tabulate(sorted([
	[dataset, d.get("train", ""), d.get("valid", ""), d.get("test", "")]
	for dataset, d in data.items()
	if d
], key=lambda x: x[0]), ["Subset", "Train", "Valid", "test"], tablefmt="github"))

df = pd.DataFrame(sorted([
	[dataset, d.get("train", 0), d.get("valid", 0), d.get("test", 0)]
	for dataset, d in data.items()
	if d
], key=lambda x: x[0]), columns=["Subset", "Train", "Valid", "test"])
print(df.set_index("Subset").sum().to_markdown())
print(df.set_index("Subset").sum().sum())