import json
import os

from argparse import ArgumentParser
from lxml import etree

parser = ArgumentParser(description="Parse scrapped html and add price data")
parser.add_argument("business", type=str, help="JSON file of businesses")
args = parser.parse_args()

with open(args.business) as f:
    yelp = json.load(f)

bs = dict((b["id"], b) for b in yelp["businesses"])
bs_set = set([b["id"] for b in yelp["businesses"]])

for path in os.listdir("data/html"):
    id, ext = os.path.splitext(path)
    if id in bs_set:
        html_parser = etree.HTMLParser()
        tree = etree.parse(open(os.path.join("data/html", path)),
                           html_parser)

        a = tree.find(".//a[@id='price_tip']")
        if a is not None:
            price = len(a.text)
        else:
            price = None

        business = bs[id]
        business["price"] = price

with open(args.business, "w") as f:
    json.dump(yelp, f)

