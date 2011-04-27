import argparse
import csv
import json
import geojson

from geojson import Feature, FeatureCollection
from geojson.geometry import Polygon
from tools import shapefile

# from shapely.geometry import Polygon, Point

parser = argparse.ArgumentParser(description="Munge data for science!")
parser.add_argument("-b", "--business", type=str,
                    default= "data/businesses/mexican.json",
                    help="Path to buisness json file")
parser.add_argument("-s", "--shapefile", type=str,
                    default="data/shapes/tr06_d00.shp",
                    help="Path to shape file")
parser.add_argument("-c", "--city", type=str,
                    default= "data/tracts/sanfrancisco.csv",
                    help="Path to city data")
args = parser.parse_args()

sf = shapefile.Reader(args.shapefile)
reader = csv.reader(open(args.city,'rU'))

tracts = set([ ('0' + r[0]) for r in reader ])

shapeRecs = sf.shapeRecords()

recs = [ sr for sr in shapeRecs if sr.record[5] == "075"]

#polys = [(rec.record[7], Polygon(rec.shape.points)) for rec in recs]

fs = []

for r in recs:
    poly = {
        "type": "Polygon",
        "coordinates": [ [p[0], p[1]] for p in r.shape.points ],
        }
    feature = {
        "id": "tract:" + r.record[7],
        "geometry": poly,
        "properties": {
            "name": "Tract " + r.record[7]
            },
        }
    fs.append(feature)

print json.dumps({"type": "FeatureCollection", "features": fs}, indent=4)

