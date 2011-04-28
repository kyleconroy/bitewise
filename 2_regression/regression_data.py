import argparse
import csv
import json
from tools import shapefile
from math import log

from shapely.geometry import Polygon, Point

parser = argparse.ArgumentParser(description="Munge data for science!")
parser.add_argument("business", type=str,
                    help="Path to business json file")
parser.add_argument("category", type=str,
                    help="category (vietnamese etc)")
parser.add_argument("ethnicity", choices=["hispanic", "asian", "white", "black"])
parser.add_argument("neighborhood", choices=["Mission", "Japantown", "Chinatown", "Civic Center/Tenderloin"])
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


sf = shapefile.Reader("../data/shapes/tr06_d00.shp")
reader = csv.reader(open("../data/tracts/sanfrancisco.csv",'rU'))

tracts = set([ ('0' + r[0]) for r in reader ])

# Reopen it now that we have our set initialized with no duplicates

reader = csv.reader(open("../data/tracts/sanfrancisco.csv",'rU'))
ethnic_data = {}
for r in reader:
    ethnic_data["0" + r[0]] = {
        "hispanic": int(r[10].replace(',','')),
        "asian": int(r[6].replace(',','')),
        "black": int(r[4].replace(',','')),
        "white": int(r[3].replace(',','')),
        "total": int(r[1].replace(',',''))
    }

shapeRecs = sf.shapeRecords()
recs = [ sr for sr in shapeRecs if sr.record[5] == "075"]
polys = [(rec.record[7], Polygon(rec.shape.points)) for rec in recs]
yelp = json.load(open(args.business))

data = {}
data["ratings"] = []
data["neighborhoods"] = []
data["percents"] = []
data["densitys"] = []
data["theils"] = []
data["prices"] = []


for business in yelp["businesses"]:
    
    b = Business(business)
    if (b.price == None):
        continue
    raw_coord = b.location["coordinate"]
    point = Point(raw_coord["longitude"], raw_coord["latitude"])
    for tag, poly in polys:
        if point.within(poly):
            data["ratings"].append(b.rating)
            ethnic_count = float(ethnic_data[tag][args.ethnicity])
            b.percentage = ethnic_count / ethnic_data[tag]["total"]
            data["percents"].append(b.percentage)
            
            b.tract = tag
            
            if b.location.has_key("neighborhoods"):
                if args.neighborhood in b.location["neighborhoods"]:
                    data["neighborhoods"].append(1)
                else:
                    data["neighborhoods"].append(0)
            else:
                data["neighborhoods"].append(0)
                
            d = ethnic_data[tag]["total"] / poly.area
            data["densitys"].append(d)
            

            data["prices"].append(float(b.price))
            
            theil = 0
            if( ethnic_data[tag]["total"] != 0):
                white_pr = float(ethnic_data[tag]["white"]) / ethnic_data[tag]["total"]
                asian_pr = float(ethnic_data[tag]["asian"]) / ethnic_data[tag]["total"]
                hispanic_pr = float(ethnic_data[tag]["hispanic"]) / ethnic_data[tag]["total"]
                black_pr = float(ethnic_data[tag]["black"]) / ethnic_data[tag]["total"]
                if (white_pr != 0.0):
                    theil += white_pr * log( 1.0 / white_pr)
                if (asian_pr != 0.0):
                    theil += asian_pr * log( 1.0 / asian_pr)
                if (hispanic_pr != 0.0):
                    theil += hispanic_pr * log( 1.0 / hispanic_pr)
                if(black_pr != 0.0):
                    theil += hispanic_pr * log( 1.0 / hispanic_pr)
                data["theils"].append(theil)
            else:
                data["theils"].append(0)


for output in data:
    writer = csv.writer(open("%s_%s.csv" % (args.category, output), "w"))
    writer.writerow([output[:-1]])
    for o in data[output]:
        writer.writerow([o])
    

