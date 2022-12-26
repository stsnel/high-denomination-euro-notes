#!/usr/bin/env python3

"""Downloads all-time banknote statistics of each country from eurobilltracker.com. Downloaded data for
   each country consists of the total number of notes, the number of notes by denomination and the average
   rate of notes entered per day for each year.
"""

import csv
import datetime
import re
import requests
import time

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

def get_total_notes(data):
    for line in data.split("\n"):
        clean_line = line.replace("<span style=\"font-size: 7px; line-height: normal\">&nbsp;</span>", "")
        if re.match(r"[\S\s]+Our users entered", clean_line):
            match_total= re.search(r"\<b\>(\d+)\<\/b\> notes in total", clean_line)
            return match_total.group(1)

def get_denomination_data(data):
    output = []
    for line in data.split("\n"):
        clean_line = line.replace("<span style=\"font-size: 7px; line-height: normal\">&nbsp;</span>", "")
        if re.match(r"[\S\s]+/img/bills/ebt\d+b.gif", clean_line):
            match_denomination = re.search(r"alt=\'(\d+)\sEUR\'[\S\s]+\<b\>(\d+)\<\/b\>", clean_line)
            output.append( { "Denomination": match_denomination.group(1),
                             "Number": match_denomination.group(2) } )
    return output


def get_rate_data(data):
    output = []
    for line in data.split("\n"):
        clean_line = line.replace("<span style=\"font-size: 7px; line-height: normal\">&nbsp;</span>", "")
        if re.match(r"[\S\s]+nowrap\>2\d{3}\<\/td\>", clean_line):
            match_rate = re.search(r"nowrap\>(2\d{3})\<\/td\>[\S\s]+\<b\>(\d+\.?\d*)\<\/b\>", clean_line)
            output.append( { "Year": match_rate.group(1),
                             "Rate": match_rate.group(2) } )
    return output

countries = get_countries()
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
first_entry = True

for country in countries:
  country_string = country.replace(" ", "+")
  endpoint = "notes/?command=8&tab=1&c=0&nocookie=1&country=" + country_string
  time.sleep(1)
  data = ""
  for n in range(20):
      print("Retrieving data for country " + country)
      data = get_request(endpoint)
      if "The statistic you requested was not completely found in the cache" in data:
          print("Waiting for data to be ready ...")
          time.sleep(10)
      else:
          break
  if "The statistic you requested was not completely found in the cache" in data:
       print("Error: could not retrieve data for country " + country)
  else:
      print("Data complete for " + country)

  with open('{}.{}.total.csv'.format(country, timestamp), 'a', newline ='') as csvfile:
      fieldnames = ["Country", "Total notes"]
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      if first_entry:
          writer.writeheader()
      writer.writerow( { "Country": country, "Total notes" : get_total_notes(data) } )

  with open('{}.{}.rateperday.csv'.format(country, timestamp), 'a', newline ='') as csvfile:
      fieldnames = ["Country", "Year", "Rate per day"]
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      if first_entry:
          writer.writeheader()
      for d in get_rate_data(data):
          writer.writerow( { "Country": country, "Year" : d["Year"], "Rate per day" : d["Rate"] } )

  with open('{}.{}.denomination.csv'.format(country, timestamp), 'a', newline ='') as csvfile:
      fieldnames = ["Country", "Denomination", "Number"]
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      if first_entry:
          writer.writeheader()
      for d in get_denomination_data(data):
          writer.writerow( { "Country": country, "Denomination" : d["Denomination"], "Number" : d["Number"] } )

  first_entry = False
