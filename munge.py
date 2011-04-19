import shapefile
import csv
import json
from shapely.geometry import Polygon, Point


sf = shapefile.Reader("tr06_d00_shp/tr06_d00.shp")
reader = csv.reader(open("data/tracts/sanfrancisco.csv",'rU'))


tracts = set([ ('0' + r[0]) for r in reader ])

# shape = sf.shape(102)
# print shape.bbox
shapeRecs = sf.shapeRecords()

recs = [ sr for sr in shapeRecs if sr.record[5] == "075"]

polys = [(rec.record[7], Polygon(rec.shape.points)) for rec in recs]

yelp = json.load(open("data/businesses/mexican.json"))

for business in yelp["businesses"]:
    raw_coord = business["location"]["coordinate"]
    point = Point(raw_coord["longitude"], raw_coord["latitude"])
    for tag, poly in polys:
        
        if point.within(poly):
            print tag, business["name"]
    
