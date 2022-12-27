#!/usr/bin/env python3

"""This script creates tables and graphs regarding relative use of high-denomination
   notes by country"""

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


def get_summary_data(eurozone=True, minimum_observations = 6000):
    total_files = glob("../../data/ebt-summary/*.*.total.csv")
    country_data = dict()
    eurozone_countries = get_eurozone_countries()
    for total_file in total_files:
        filename_parts = os.path.basename(total_file).split(".")
        country = filename_parts[0]
        timestamp = filename_parts[1]
        num_observations = 0

        if (country in eurozone_countries) != eurozone:
            continue

        with open(total_file, "r") as infile:
            reader = csv.reader(infile)
            for row in reader:
                if row[1] == "Total notes":
                    continue
                num_observations = int(row[1])
                break
           
        if num_observations < minimum_observations:
            continue

        denom_file = "../../data/ebt-summary/{}.{}.denomination.csv".format(country, timestamp)
        with open(denom_file, "r") as infile:
            reader = csv.reader(infile)
            data = dict()
            data["Total"] = num_observations
            for row in reader:
                data[row[1]] = row[2]
            country_data[country] = data

    return country_data


def absolute_to_relative(data):
    outdata = dict()
    for country, country_data in data.items():
        out_country_data = dict()
        for label, value in country_data.items():
            if value == "Number":
                continue
            if label == "Total":
                out_country_data[label] = int(value)
            else:
                out_country_data[label] = round(100* int(value) / int(country_data["Total"]), 1)
        outdata[country] = out_country_data
    return outdata


def get_last_data(eurozone=True, minimum_observations = 300):
    last_files = glob("../../data/ebt-last-notes/*.*.csv")
    country_data = dict()
    eurozone_countries = get_eurozone_countries()
    for last_file in last_files:
        filename_parts = os.path.basename(last_file).split(".")
        country = filename_parts[0]
        timestamp = filename_parts[1]
        num_observations = 0
        observations = dict()

        if (country in eurozone_countries) != eurozone:
            continue

        with open(last_file, "r") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                denomination = row["Notetype"]
                num_observations += 1
                if denomination in observations:
                    observations[denomination] += 1
                else:
                    observations[denomination] = 1

        if num_observations >= minimum_observations:
            observations["Total"] = num_observations
            country_data[country] = observations

    return country_data


def get_color_dict():
    return {   "5": "darkgreen",
               "10": "red",
               "20": "blue",
               "50": "orange",
               "100": "lightgreen",
               "200": "yellow",
               "500": "purple" }


def plot_data(data, outfile, title):
    countries = sorted(data.keys())
    color_dict = get_color_dict()
    plots = []
    denominations = ["5", "10", "20", "50", "100", "200", "500"]
    denomination_labels = list(map(lambda d: d + " euro", denominations))
    cumulative_data = dict()
    table_data = dict()
    fig = plt.gcf()
    plt.gca().invert_yaxis()
    fig.set_size_inches(18.5, 10.5)
    for denomination in denominations:
        denom_data = []
        table_data[denomination] = dict()
        color = color_dict[denomination]
        lefts = []
        for country in countries:
            table_data[country] = dict()
            this_data = data[country].get(denomination, 0)
            table_data[denomination][country] = this_data
            if country in cumulative_data:
                left = cumulative_data[country]
                cumulative_data[country] += this_data
            else:
                left = 0
                cumulative_data[country] = this_data
            lefts.append(left)
            denom_data.append(data[country].get(denomination, 0))
        plot = plt.barh(countries, denom_data, color=color, left=lefts)
        plots.append(plot)
    plt.title(title)
    plt.legend(plots, denomination_labels, title="Denominations", loc="lower left")
    plt.tight_layout()
    plt.savefig(outfile)
    plt.clf()
    print()
    print(title +":")
    print()
    print("|Country|5 euro|10 euro|20 euro|50 euro|100 euro|200 euro|500 euro|")
    print("|-------|------|-------|-------|-------|--------|--------|--------|")
    for country in sorted(countries):
        print("|{}|{}|{}|{}|{}|{}|{}|{}|".format(country,
                table_data["5"][country],
                table_data["10"][country],
                table_data["20"][country],
                table_data["50"][country],
                table_data["100"][country],
                table_data["200"][country],
                table_data["500"][country]))

eurozone_data = absolute_to_relative(get_summary_data(eurozone=True))
nonez_data = absolute_to_relative(get_summary_data(eurozone=False))
plot_data(eurozone_data, "../../plots/eurozone-summary.png", "Tracked notes by denomination by country (inside eurozone)")
plot_data(nonez_data, "../../plots/non-eurozone-summary.png","Tracked notes by denomination by country (outside eurozone)")
eurozone_last_data = absolute_to_relative(get_last_data(eurozone=True))
nonez_last_data = absolute_to_relative(get_last_data(eurozone=False))
plot_data(eurozone_last_data, "../../plots/eurozone-last.png", "Last tracked notes by denomination by country (inside eurozone)")
plot_data(nonez_last_data, "../../plots/non-eurozone-last.png","Last tracked notes by denomination by country (outside eurozone)")
