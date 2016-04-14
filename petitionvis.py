#!venv/bin/python
import sys
import json
from operator import methodcaller
from pathlib import Path
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Usage: petitionvis.py <petition number>")
    sys.exit(1)

p = Path("{0}.json".format(sys.argv[1]))
if not p.exists():
    print("'{0}' does not exist!".format(str(p)))
    sys.exit(1)

petition = None
with p.open() as f:
    petition = json.load(f)["data"]

petition_id = petition["id"]
petition = petition["attributes"]
# print(*[k for k in petition.keys()], sep=", ")

action = petition["action"]
print("Action:", action)

print("Author:", petition["creator_name"])

signum = petition["signature_count"]
print("Signum:", signum)

sigs_by_country = petition["signatures_by_country"]
sigs_by_constituency = petition["signatures_by_constituency"]

# Sort countries by number of signatures
sigs_by_country.sort(key=methodcaller("get", "signature_count"), reverse=True)

signum_uk = [country["signature_count"] for country in sigs_by_country
             if country["name"] == "United Kingdom"][0]
labels = ["UK", "Other"]
colors = ["#5DA5DA", "#FAA43A", "#60BD68", "#B276B2", "#DECF3F", "#F15854"]
boom = (0, 0.5)
sizes = [signum_uk / signum * 100, (signum - signum_uk) / signum * 100]
plt.figure(figsize=(16, 12))
plt.pie(sizes, labels=labels, colors=colors, explode=boom, autopct="%1.1f%%",
        pctdistance=0.8)
plt.suptitle("{0}, '{1}', {2}\nPercentage of signatures from the UK vs other countries".format(petition_id, action, signum))
plt.axis("equal")
plt.savefig("{0}_{1}_sigPercentagesUKvsOther.png".format(petition_id, signum))
plt.close()

sigs_by_country_sans_uk = [country for country in sigs_by_country
                           if country["code"] != "GB"]
signum_other = signum - signum_uk
labels = [country["name"] for country in sigs_by_country_sans_uk
          if country["signature_count"] >= 20]
colors = ["#5DA5DA", "#FAA43A", "#60BD68", "#B276B2", "#DECF3F", "#F15854"]
sizes = [country["signature_count"] / signum_other * 100 for country
         in sigs_by_country_sans_uk if country["signature_count"] >= 20]
plt.figure(figsize=(16, 12))
plt.pie(sizes, labels=labels, colors=colors, labeldistance=1.12, startangle=90,
        autopct="%1.1f%%", pctdistance=1.06)
plt.suptitle("{0}, '{1}', {2}\nPercentages of signatures from other countries (where signature count >= 20)".format(petition_id, action, signum))
plt.axis("equal")
plt.savefig("{0}_{1}_sigPercentagesOther.png".format(petition_id, signum))
plt.close()
