from tabulate import tabulate
import os.path
import glob

headers = ["", "train", "valid", "test"]

rows = []

for subset in glob.glob("./data/*"):
	sub = os.path.basename(subset)
	row = [""] * 4
	row[0] = sub
	for split in glob.glob(f"{subset}/*"):
		spl = os.path.basename(split)
		row[headers.index(spl)] = str(len(glob.glob(f"{subset}/{spl}/labels/*.txt")))
	rows.append(row)

rows = [headers] + sorted(rows, key=lambda x: int(x[1]) if x[1] else 0)


print(tabulate(rows, headers="firstrow", tablefmt="github"))