import argparse
import csv
import json
import os

parser = argparse.ArgumentParser(description="Munge data for science!")
parser.add_argument("-b", "--business", type=str,
                    default= "data/businesses",
                    help="Path to buisness json file")
args = parser.parse_args()

def get_geojson(businesses):
    fs = []
    for b in businesses:
        coords = b["location"]["coordinate"]
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


