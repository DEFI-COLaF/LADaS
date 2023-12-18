from util import rel_path
import glob
import tqdm


def yolobbox2bbox(minx, miny, maxx, maxy):
    w = maxx - minx
    h = maxy - miny
    cx = minx + w/2
    cy = miny + h/2
    return cx, cy, w, h


def detect(path: str = "data*/*/labels/*.txt"):
    wrong = []
    for file in tqdm.tqdm(glob.glob(rel_path(path))):
        with open(file) as f:
            for line in f:
                if len(line.strip().split()) > 5:
                    wrong.append(file)#, line.strip().split()[1:]))
                    break
    return wrong


def correct(file):
    lines = []
    with open(file) as f:
        for line in f:
            line = line.strip().split()
            if len(line) > 5:
                cls, *xys = line
                xys = list(map(float, xys))
                xs = xys[::2]
                ys = xys[1::2]
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)
                lines.append([cls, *yolobbox2bbox(min_x, min_y, max_x, max_y)])
            else:
                lines.append(line)

    with open(file, "w") as f:
        f.write("\n".join([" ".join([str(v) for v in line]) for line in lines]))
    print(f"Corrected {file}")


for wrong_file in detect():
    correct(wrong_file)
