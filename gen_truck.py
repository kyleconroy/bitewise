import argparse
import csv
import json
import os

class Truck(object):

    def __init__(self, row):
        self.cnn = row[0]
        self.id = row[1]
        self.applicant = row[2]
        self.facility_type = row[3]
        self.location = row[4]
        self.full_address = row[5]
        self.block_lot = row[6]
        self.block = row[7]
        self.lot = row[8]
        self.permit = row[9]
        self.status = row[10]
        self.food_items = row[11]
        self.x = row[12]
        self.y = row[13]
        self.lat = float(row[14])
        self.long = float(row[15])
        self.schedule = row[16]


def get_geojson(truck):
    poly = {
        "type": "Point",
        "coordinates": [ truck.long, truck.lat ],
        }
    feature = {
        "id": truck.id,
        "geometry": poly,
        "properties": truck.__dict__,
        }
    return feature

fs = []

for r in csv.reader(open("data/mobilefoodpermits.csv")):
    try:
        truck = Truck(r)
        if truck.long and truck.lat:
            fs.append(get_geojson(truck))
    except:
        pass

with open("data/geojson/trucks.json", "w") as out:
    json.dump({"type": "FeatureCollection", "features": fs}, out, indent=4)


