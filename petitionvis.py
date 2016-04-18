#!venv/bin/python
import sys
import json
from operator import methodcaller
from pathlib import Path
import shapefile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection

if len(sys.argv) != 2:
    print("Usage: petitionvis.py <petition number>")
    sys.exit(1)

p = Path("{0}.json".format(sys.argv[1]))
if not p.exists():
    print("'{0}' does not exist!".format(str(p)))
    sys.exit(1)

print("Loading petition...")
with p.open() as f:
    petition_json = json.load(f)["data"]

petition_id = petition_json["id"]
petition = petition_json["attributes"]
# print(*[k for k in petition.keys()], sep=", ")

action = petition["action"]
author = petition["creator_name"]
signum = petition["signature_count"]

print("Action:", action)
print("Author:", author)
print("Signum:", signum)

# Make map
print("Making map:")
fig = plt.figure(figsize=(12, 16))
ax = fig.gca()
print("Setting up map...")
plt.title("{0}, {1}, {2}\nVotes by Constituency".format(petition_id, action, signum))
m = Basemap(resolution="h", projection="merc",
            llcrnrlon=-10.6, llcrnrlat=49.9, urcrnrlon=1.9, urcrnrlat=59.4, ax=ax)
m.drawcoastlines(linewidth=0.75)
m.drawcountries(linewidth=0.5)
print("Loading shapefile...")
m.readshapefile("westminster_const_region", "constituencies", linewidth=0.25)
lon, lat = -3.034, 51.8246
x, y = m(lon, lat)
ax.plot(x, y, "ro", markersize=3)

print("Saving map...")
plt.savefig("fig/{0}_{1}_map.png".format(petition_id, signum), dpi=300)
plt.close()
