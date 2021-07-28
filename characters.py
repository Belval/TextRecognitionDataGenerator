import os
from argparse import ArgumentParser

def main(args):
    file_name = "labels.txt"
    file_path = os.path.join(args.i, file_name)
    lines = []
    with open(file_path) as f:
        lines = f.readlines()
    words = []
    for line in lines:
        words.append(line.split(".jpg ")[1].split("\n")[0])
    str = ""
    for word in words:
        str = str + word
    #print(str)
    print(list(set(str)))
    return

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--i", type=str, required=True, help="Input dir")
    args = parser.parse_args()
    main(args)