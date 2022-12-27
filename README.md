# Tracking statistics for high-denomination euro banknotes

## Banknotes in circulation versus practical use

The euro has seven banknote denominations: 5, 10, 20, 50, 100, 200 and 500 euro.

Official circulation data indicates that the 5, 10, 20, 50 and 100 euro notes are most common [1].
The 200 and 500 euro notes are less common relative to the other denominations, but together
they still make up roughly 3% of all Euro banknotes in circulation.

![image](plots/ecb-circulation.png)

| 5 euro | 10 euro | 20 euro | 50 euro | 100 euro | 200 euro| 500 euro|
|---|---|---|---|---|---|---|
| 7.2% | 10.1% | 16.1% | 49.1% | 13.5% | 2.0% | 1.0% | 

The circulation data seems to differ from how the denominations are used
in practice in some countries. For example, in The Netherlands, only the 5, 10, 20 and 50 euro
notes are in everyday use in most areas. These lower-denomination notes are available in ATMs and generally accepted by
shops. In a 2021 survey, the Dutch national bank (DNB) found that a majority of respondents
had never held a 200 euro note and/or a 500 euro note [2]. Although a majority had held a 100 euro
note, most people did not have one in the past year.

This begs the question where all of these high-denomination notes are, if people use them only
rarely. This document uses data from https://eurobilltracker.com to show in which countries high-denomination
euro banknotes are reportedly used most frequently, both relative to low-denomination notes and
in absolute numbers. The repository also contains the processed data and scripts that were used
to create the graphs and tables.

## Summary data

The tables and plots show the Eurobilltracker denomination data by country over the past (roughly) 20 years.
Only countries with more than 6000 notes entered (on average, roughly 300 per year) have been included. Data
for countries inside and outside the eurozone is listed in separate tables and plots.

|Country|5 euro|10 euro|20 euro|50 euro|100 euro|200 euro|500 euro|
|-------|------|-------|-------|-------|--------|--------|--------|
|Andorra|37.4|21.6|19.1|14.8|6.0|0.5|0.7|
|Austria|44.1|31.9|11.2|7.0|4.7|0.6|0.5|
|Belgium|45.3|18.7|20.9|13.4|1.2|0.2|0.3|
|Cyprus|42.5|17.9|26.1|11.7|1.5|0.1|0.2|
|Estonia|57.3|19.2|15.2|8.0|0.2|0.1|0.1|
|Finland|33.6|19.6|31.9|13.5|1.0|0.2|0.3|
|France|33.7|29.4|26.5|9.4|0.9|0.1|0.1|
|Germany|52.6|22.0|12.5|10.6|1.8|0.2|0.3|
|Greece|26.9|20.0|24.3|26.1|2.2|0.1|0.2|
|Ireland|37.3|26.5|23.6|12.2|0.3|0.0|0.0|
|Italy|27.1|22.8|24.5|23.2|2.1|0.1|0.2|
|Latvia|28.8|25.3|24.5|20.4|0.8|0.1|0.2|
|Lithuania|51.8|18.8|11.9|13.0|3.9|0.5|0.1|
|Luxembourg|33.0|25.3|23.3|15.3|2.2|0.6|0.6|
|Malta|14.8|40.9|30.5|12.5|0.8|0.2|0.3|
|Monaco|51.9|13.6|15.9|12.8|4.6|0.7|0.5|
|Netherlands|36.9|29.2|18.7|14.0|0.9|0.2|0.1|
|Portugal|23.9|30.7|37.4|6.5|1.0|0.2|0.2|
|San Marino|40.9|22.9|19.6|14.3|2.1|0.2|0.0|
|Slovakia|27.3|32.7|18.4|14.1|6.4|0.4|0.7|
|Slovenia|31.7|25.4|28.9|9.9|3.3|0.3|0.6|
|Spain|25.5|23.3|26.1|23.2|1.3|0.2|0.4|
|Vatican City|21.2|17.0|16.3|37.4|7.4|0.4|0.2|

![image](plots/eurozone-summary.png)

|Country|5 euro|10 euro|20 euro|50 euro|100 euro|200 euro|500 euro|
|-------|------|-------|-------|-------|--------|--------|--------|
|Belarus|25.7|23.5|33.6|12.4|4.0|0.5|0.4|
|Bosnia-Herzegovina|35.5|22.5|17.8|17.1|6.2|0.6|0.4|
|Brazil|10.4|14.2|17.5|31.5|17.2|1.5|7.6|
|Bulgaria|12.7|16.4|18.5|37.7|11.8|1.7|1.1|
|Canada|23.7|18.8|34.1|18.2|3.9|0.5|0.8|
|China|13.6|15.2|18.4|25.0|20.5|1.2|6.0|
|Croatia|17.3|21.7|20.5|22.9|13.2|1.5|3.0|
|Czech Republic|27.6|26.8|20.3|16.1|7.2|1.1|0.9|
|Denmark|23.8|22.2|30.8|18.1|4.0|0.7|0.4|
|Dominican Republic|6.2|7.5|17.0|43.4|15.1|2.1|8.7|
|Hungary|22.3|27.3|20.1|20.9|8.0|0.6|0.8|
|Japan|25.3|30.1|25.3|15.7|3.2|0.2|0.1|
|Montenegro|22.8|33.6|16.6|23.8|2.8|0.1|0.2|
|Norway|25.0|19.0|26.0|23.0|6.0|0.3|0.5|
|Poland|28.3|21.1|17.6|23.7|8.2|0.5|0.6|
|Romania|25.4|19.8|20.6|23.8|8.2|0.6|1.5|
|Russia|11.9|12.0|13.7|21.0|33.2|1.6|6.6|
|Serbia|23.1|25.9|22.4|18.7|8.1|0.9|1.0|
|Sweden|29.2|24.2|30.7|13.1|2.3|0.3|0.2|
|Switzerland|42.1|15.3|15.0|18.6|6.5|1.5|1.1|
|Turkey|24.2|26.4|21.8|18.6|6.3|1.5|1.3|
|Ukraine|8.1|9.3|9.9|39.3|29.8|1.5|2.0|
|United Kingdom|9.8|30.0|44.5|13.9|1.5|0.2|0.1|
|United States|28.6|22.7|27.3|17.2|3.3|0.3|0.5|

![image](plots/non-eurozone-summary.png)

The data shows that high-denomination notes occur with low frequency (less than, say, 1.5% of observed
notes) in some eurozone countries, including France, Ireland, Netherlands and Portugal. The frequencies
for Germany and Belgium are slightly higher. Within the eurozone, Austria, Lithuania, Luxembourg, Slovakia
and Slovenia stand out as countries with fairly high frequencies of high-denomination notes (up to roughly 8%).

Some countries outside the Eurozone have a frequency distribution of high-denomination notes that is fairly
similar to the eurozone countries. This is the case for Japan, Sweden, the United Kingdom and the United States.
Other non-eurozone countries have relatively high frequencies for the high-denomination notes. The most extreme
figures are those of Russia and Ukraine, where more than one in three observed notes is a high-denomination note.
The Dominican Republic, China, Brazil, as well as various central European and southeast European countries outside
the eurozone also have quite high rates for high-denomination notes, relative to the eurozone countries.

## Sources

* [1] *Banknotes and coins circulation* (2022). European Central Bank (ECB).
      https://www.ecb.europa.eu/stats/policy_and_exchange_rates/banknotes+coins/circulation/html/index.en.html
* [2] *Bekendheid en Waardering Bankbiljetten* (2021). De Nederlandse Bank (DNB), in Dutch. Page 11.
      https://www.dnb.nl/media/xyldnnnt/bekendheid-en-waardering-bankbiljetten.pdf


## License

Creative Commons CC-BY-SA 4.0 license; see
https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt or enclosed
LICENSE file
