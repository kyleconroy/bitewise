import argparse
import csv
import json
from tools import shapefile

from shapely.geometry import Polygon, Point

parser = argparse.ArgumentParser(description="Munge data for science!")
parser.add_argument("business", type=str,
                    help="Path to buisness json file")
parser.add_argument("ethnicity", choices=["mexican", "asain", "white", "black"])
args = parser.parse_args()

class Business(object):
    def __init__(self, business_dict):
        self.__dict__.update(business_dict)
        self.get_rating()

    def get_rating(self):
        url = self.rating_img_url
        if "stars_5" in url:
            self.rating = 8
        elif "stars_4_half" in url:
            self.rating = 7
        elif "stars_4" in url:
            self.rating = 6
        elif "stars_3_half" in url:
            self.rating = 5
        elif "stars_3" in url:
            self.rating = 4
        elif "stars_2_half" in url:
            self.rating = 3
        elif "stars_2" in url:
            self.rating = 2
        elif "stars_1_half" in url:
            self.rating = 1
        else:
            self.rating = 0


sf = shapefile.Reader("tr06_d00_shp/tr06_d00.shp")
reader = csv.reader(open("data/tracts/sanfrancisco.csv",'rU'))

tracts = set([ ('0' + r[0]) for r in reader ])

reader = csv.reader(open("data/tracts/sanfrancisco.csv",'rU'))
ethnic_data = {}
for r in reader:
    ethnic_data["0" + r[0]] = {
        "mexican": int(r[10].replace(',','')),
        "asian": int(r[6].replace(',','')),
        "black": int(r[4].replace(',','')),
        "white": int(r[3].replace(',','')),
        "total": int(r[1].replace(',',''))
    }

shapeRecs = sf.shapeRecords()

recs = [ sr for sr in shapeRecs if sr.record[5] == "075"]

polys = [(rec.record[7], Polygon(rec.shape.points)) for rec in recs]

yelp = json.load(open(args.business))

x = []
y = []




for business in yelp["businesses"]:

    b = Business(business)

    raw_coord = b.location["coordinate"]
    point = Point(raw_coord["longitude"], raw_coord["latitude"])
    for tag, poly in polys:
        if point.within(poly):
            ethnic_count = float(ethnic_data[tag][args.ethnicity])
            b.percentage = ethnic_count / ethnic_data[tag]["total"]
            b.tract = tag

            x.append(b.percentage)
            y.append(b.rating)


writer = csv.writer(open("data/rdata/%s_percents.csv" % args.ethnicity, "w"))
writer.writerow(["percent"])
for percent in x:
    writer.writerow([percent])

# Write y axis
writer = csv.writer(open("data/rdata/%s_ratings.csv" % args.ethnicity, "w"))
writer.writerow(["rating"])
for rating in y:
    writer.writerow([rating])
