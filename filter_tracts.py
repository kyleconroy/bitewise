import json

calif_tracts_data = open('tracts.json')

calif_tracts = json.load(calif_tracts_data)

sf_tracts = []
for r in calif_tracts["features"]:
    if r["properties"]["COUNTY"] == "075":
        sf_tracts.append(r)

calif_tracts_data.close()
print json.dumps({"type": "FeatureCollection", "features": sf_tracts})