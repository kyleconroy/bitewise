import argparse
import csv
import json

parser = argparse.ArgumentParser(description="Munge data for science!")
parser.add_argument("business", type=str,
                    help="Path to buisness json file")
parser.add_argument("neighborhood", choices=["Japantown", "Mission", "Chinatown"])
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


yelp = json.load(open(args.business))

ratings = []
neighborhood_flags = []

for business in yelp["businesses"]:
    b = Business(business)
    ratings.append(b.rating)
    if b.location.has_key("neighborhoods"):
        if args.neighborhood in b.location["neighborhoods"]:
            neighborhood_flags.append(1)
        else:
            neighborhood_flags.append(0)
    else:
        neighborhood_flags.append(0)


writer = csv.writer(open("%s_ratings.csv" % (args.neighborhood), "w"))
writer.writerow(["rating"])
for rating in ratings:
    writer.writerow([rating])
    
# Write y axis
writer = csv.writer(open("%s_neighborhoods.csv" % (args.neighborhood), "w"))
writer.writerow(["neighborhood"])
for n in neighborhood_flags:
    writer.writerow([n])
