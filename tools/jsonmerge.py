import argparse
import json
import os

parser = argparse.ArgumentParser(description="Merge all the json files "
                                 "in a directory into one object")
parser.add_argument("directory", type=str, help="Directory to merge")
args = parser.parse_args()

if not os.path.isdir(args.directory):
    parser.error("Path is not a directory")

results = []

for f in os.listdir(args.directory):
    file, ext = os.path.splitext(f)
    if ext == ".json":
        with open(os.path.join(args.directory, f)) as js:
            results.extend(json.load(js)["businesses"])

filename = "{}{}".format(args.directory, ".json")
with open(filename, "w") as output:
    json.dump({"businesses": results}, output)
