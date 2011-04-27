import argparse
import csv
import json
import os
import logging

parser = argparse.ArgumentParser(description="Munge data for science!")
parser.add_argument("-b", "--business", type=str,
                    default= "data/businesses",
                    help="Path to buisness json file")
parser.add_argument("-d", "--debug", default=False,
                    action="store_true",
                    help="Turn on debug output")
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)

def get_rating(url):
    if "stars_5" in url:
        return 8
    elif "stars_4_half" in url:
        return 7
    elif "stars_4" in url:
        return 6
    elif "stars_3_half" in url:
        return 5
    elif "stars_3" in url:
        return 4
    elif "stars_2_half" in url:
        return 3
    elif "stars_2" in url:
        return 2
    elif "stars_1_half" in url:
        return 1
    else:
        return 0

def get_geojson(businesses):
    fs = []
    for b in businesses:
        coords = b["location"]["coordinate"]
        rating = get_rating(b["rating_img_url"])
        b["rating"] = rating
        poly = {
            "type": "Point",
            "coordinates": [ coords["longitude"], coords["latitude"]],
            }
        feature = {
            "id": b["id"],
            "geometry": poly,
            "properties": b,
            }
        fs.append(feature)
    return fs

for b in os.listdir(args.business):
    filename, ext = os.path.splitext(b)
    if ext == ".json":
        path = os.path.join(args.business, b)
        with open(path) as f:
            geo = get_geojson(json.load(f)["businesses"])
            with open("data/geojson/" + b, "w") as out:
                json.dump({"type": "FeatureCollection", "features": geo}, out, indent=4)


