#!/usr/bin/env python3

"""Generates plots of distribution of of high-denomination banknotes by country/area."""


import csv
from glob import glob
import math
import os

from matplotlib import pyplot as plt

def get_eurozone_countries():
    countries = [ "Andorra", "Austria", "Belgium", "Cyprus", "Estonia", "Finland", "France",
                  "Germany", "Greece", "Ireland", "Italy", "Latvia", "Lithuania",
                  "Luxembourg", "Malta", "Monaco", "Netherlands", "Portugal", "San Marino",
                  "Slovakia", "Slovenia", "Spain", "Vatican City" ]
    return set(countries)


def get_separate_countries():
    """Countries with a high number of high-denomination notes to show separately in plots"""
    return set(["Austria", "Germany"])


def get_high_denominations():
    return ["100", "200", "500"]


def get_data(denomination):
    denom_files = glob("../../data/ebt-summary/*.*.denomination.csv")
    data = dict()
    eurozone_countries = get_eurozone_countries()
    separate_countries = get_separate_countries()
    for denom_file in denom_files:
        filename_parts = os.path.basename(denom_file).split(".")
        country = filename_parts[0]
        timestamp = filename_parts[1]
        
        if country in separate_countries:
            label_country = country
        elif country in eurozone_countries:
            label_country = "Other eurozone countries"
        else:
            label_country = "Outside eurozone"

        num_denomination = 0
        with open(denom_file, "r") as infile:
            reader = csv.reader(infile)

            for row in reader:
                if row[1] == denomination:
                    num_denomination = int(row[2])

        if label_country in data:
            data[label_country] += num_denomination
        else:
            data[label_country] = num_denomination
    return data


def plot_data(data, title, imagefile):
    countries = []
    numbers = []
    for country, number in data.items():
        countries.append(country)
        numbers.append(number)
    plt.title(title)
    p,t, _ = plt.pie(numbers, autopct='%1.0f%%',
        shadow=False, startangle=-270, counterclock=False)
    plt.legend(p, countries, loc='upper right', bbox_to_anchor=(1.05,0.18))
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    plt.savefig(imagefile)
    plt.clf()

for denomination in get_high_denominations():
    title = "Percentage of observed notes by country - {} euro".format(denomination)
    imagefile = "../../plots/ebt-absolute-{}-euro".format(denomination)
    data = get_data(denomination)
    plot_data(data, title, imagefile)
