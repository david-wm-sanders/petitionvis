#!venv/bin/python
import sys
import json
from operator import methodcaller
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

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

# Create a dictionary of ons_code:signature_count
sigcount_by_constcode = {c["ons_code"]: c for c in petition["signatures_by_constituency"]}

# Find the highest number of signatures
sigs_by_constituency = petition["signatures_by_constituency"]
sigs_by_constituency.sort(key=methodcaller("get", "signature_count"), reverse=True)
high_sigcount = sigs_by_constituency[0]["signature_count"]
high_sigcount = high_sigcount + high_sigcount * 0.25

# Make map
print("Making map:")
fig = plt.figure(figsize=(12, 16))
ax = fig.gca()
print("Setting up map...")
plt.title("{0}, {1}, {2}\nVotes by Constituency".format(petition_id, action, signum))
m = Basemap(resolution="h", projection="merc",
            llcrnrlon=-10.6, llcrnrlat=49.9, urcrnrlon=1.9, urcrnrlat=59.4, ax=ax)
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.25)
print("Loading shapefile...")
m.readshapefile("westminster_const_region", "constituencies", linewidth=0.25, drawbounds=False)
print("Processing shapefile...")
for info, shape in zip(m.constituencies_info, m.constituencies):
    ons_code = info["CODE"]
    sigcount = sigcount_by_constcode[ons_code]["signature_count"]
    p = Polygon(np.array(shape), linewidth=0.1, ec="k", fc=str(1 - sigcount / high_sigcount))
    ax.add_patch(p)

print("Saving map...")
plt.savefig("fig/{0}_{1}_map.png".format(petition_id, signum), dpi=300)
plt.close()
