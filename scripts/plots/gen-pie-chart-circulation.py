#!/usr/bin/env python3

"""Generates a pie chart of banknote denominations by relative circulation.
"""

import csv
import matplotlib.pyplot as plt

datafilename = "../../data/ecb/ecb-circulation-denominations-percent-nov2022.csv"

color_dict = { "5": "darkgreen",
               "10": "red",
               "20": "blue",
               "50": "orange",
               "100": "lightgreen",
               "200": "yellow",
               "500": "purple" }
               
labels = []
circulation = []
colors = []
explode = []

with open(datafilename, "r") as datafile:
    reader = csv.DictReader(datafile, delimiter=";")
    for row in reader:
        labels.append(row["Denomination"] + " euro")
        colors.append(color_dict[row["Denomination"]])
        circulation.append(row["Percent"])
        explode.append(0.025 if row["Denomination"] in ["100","200","500"] else 0)

plt.title("Relative circulation of euro banknotes, ECB data of November 2022")
p,t = plt.pie(circulation, explode=explode, colors=colors,
        shadow=False, startangle=-270, counterclock=False)
plt.legend(p, labels, loc='right', bbox_to_anchor=(1.10,0.5))
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.tight_layout()
plt.savefig("../../plots/ecb-circulation.png")
