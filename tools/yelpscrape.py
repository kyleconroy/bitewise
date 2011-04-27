import argparse
import json
import logging
import os
import time
import urllib

logging.basicConfig(level=logging.DEBUG, filename="scrape.log")

def scrape(s, output_dir):
    url = s["url"]
    try:
        result = urllib.urlopen(url)
        filename = s["id"] + ".html"
        path = os.path.abspath(os.path.join(output_dir, filename))
        logging.debug(path)
        with open(path, "w") as f:
            f.write(result.read())
    except:
        logging.error("Could not read {}".format(url))

parser = argparse.ArgumentParser(description="Scrape yelp for data")
parser.add_argument("input_dir", type=str,
                    help="Directory of json files from the yelp api")
parser.add_argument("output_dir", type=str,
                    help="Directory to save html files")
args = parser.parse_args()

for j in os.listdir(os.path.abspath(args.input_dir)):
    filename, ext = os.path.splitext(j)
    if ext == ".json":
        with open(os.path.abspath(os.path.join(args.input_dir, j))) as f:
            for s in json.load(f)["businesses"]:
                scrape(s, args.output_dir)
                time.sleep(2)

