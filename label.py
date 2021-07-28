import os
from argparse import ArgumentParser

def main(args):
    file_name = "labels.txt"
    file_path = os.path.join(args.i, file_name)
    lines = []
    with open(file_path) as f:
        lines = f.readlines()
    for line in lines:
        image_no = line.split(".jpg ")[0]
        words = line.split(".jpg ")[1]
        f = open(f"{image_no}.txt", "a")
        f.write(f"{words}")
        f.close()

    return

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--i", type=str, required=True, help="Input dir")
    args = parser.parse_args()
    main(args)
    