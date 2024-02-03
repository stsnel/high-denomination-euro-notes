#!/usr/bin/env python3

"""Downloads data of last (up to) 330 banknotes entered in the last year for each country from EuroBillTracker.com
"""

import argparse
import csv
import datetime
import re
import requests
import time

def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument('--year', default=2023, type=int,
                        help="Cut off year (notes that were seen before this year are discarded)")
    return parser.parse_args()

def get_request(endpoint):
    headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36" }
    url = "https://en.eurobilltracker.com/" + endpoint
    response = requests.post(url, headers=headers)
    return response.content.decode('utf-8')

def get_countries():
    countries = []
    for line in get_request("notes").split("\n"):
        match = re.match(r"^\<option\svalue\=\"([\w\s\-]+)\"\>", line)
        if match:
            countries.append(match.group(1))
    return [ country for country in countries if "---" not in country ]

args = parse_args()
countries = get_countries()
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

for country in countries:
  time.sleep(1)
  with open('{}.{}.csv'.format(country, timestamp) , 'w', newline='') as csvfile:
    fieldnames = ["Date", "Time", "Notetype", "Maskedserial", "Locality"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    bills = []
    last_year = 0
    for n in range(11):
        country_string = country.replace(" ", "+")
        endpoint = f"notes/?cursor={str(n)};country={country_string};timescale=M_DAYS"
        for line in get_request(endpoint).split("\n"):
            if re.match(r"\<TR\sbgcolor=\'\#\w+\'\>\<TD\sclass\=\'smallRightTD\'", line):
                data = dict()
                match_datetime = re.search(r"nowrap\>(\d{4}\-\d{2}\-\d{2})\s(\d{2}:\d{2}:\d{2})\<\/TD", line)
                if match_datetime:
                    data["Date"] = match_datetime.group(1)
                    data["Time"] = match_datetime.group(2)
                    last_year = int(match_datetime.group(1).split("-")[0])
                match_notetype = re.search(r"alt\=\'(\d+)\ EUR\'", line)
                if match_notetype:
                    data["Notetype"] = match_notetype.group(1)
                match_maskedserial = re.search(r"href\=\"\/notes\/\?id\=\d+\;PHPSESSID=\S+\"\>(\S+)\<\/a\>", line)
                if match_maskedserial:
                    data["Maskedserial"] = match_maskedserial.group(1)
                match_locality = re.search(r"href\=\"\/profile\/\?city\=\d+\;PHPSESSID=\S+\"\>([\w\-\s]+)\<\/a\>", line)
                if match_locality:
                    data["Locality"] = match_locality.group(1)
                print(str(data))
                if last_year < args.year:
                    break
                writer.writerow(data)
