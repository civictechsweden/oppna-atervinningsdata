# Öppna återvinningsdata (Open recycling data)

This python script can automatically fetch all the Swedish recycling stations (återvinningsstationer) using Avfall Sverige's open APIs. It also fetches the station "service info", which means basic information about when containers are emptied and in some cases information about cleaning, snow ploughing.

It exports the result as JSON or CSV in the data folder.

On this repository, you can download the data directly. It is updated monthly by Github Actions every night at 1AM EST.

The data is updated continuously by Avfall Sverige. The data made available by this hobby project might be outdated, or inaccurate.

License for the code is AGPL 3.0, license for the data is CC0 (but attribution is appreciated).

## Why?

I started this project two years ago to fill in a gap, when FTI AB was still in charge of recycling data. The list of recycling stations often comes up among the most requested datasets in Sweden. Although the information is well structured and made available nationally through open APIs and a user-friendly map by Avfall Sverige on [sopor.nu](https://www.sopor.nu) (previously by FTI AB), it is not available as open data.

And since these organisations aren't part of the public sector, open data is even less of a priority for them than it is for government organisations.

Therefore, introducing Öppna återvinningsdata.

UPDATE July 2024: FTI AB has now completely transferred its mandate to the new Swedish waste portal (*Sveriges avfallsportal*, at [sopor.nu](https://www.sopor.nu)). That means that their APIs do not work anymore and I've updated my code to use the new portal's API. Good news is they are much better! They use the modern standard REST (instead of SOAP for FTI AB) and there is no need anymore to parse data from HTML. The variable naming is still a bit obscure though and there is no documentation so this project is still useful in order to understand which API endpoints exist, what data format they return and what some values stand for.

For instance, here is a correspondence table for service ids:

- 1: Pappersförpackningar
- 2: Plastförpackningar
- 3: Metallförpackningar
- 4: Ofärgade glasförpackningar
- 5: Färgade glasförpackningar
- 6: Tidningar och andra trycksaker
- 7: Batterier
- 8: Textil
- 9: Städning

## Installation

- Install Python 3 on your machine if you don't already have it.

- Install the dependencies

```python
pip install -r requirements.txt
```

## Usage

- Import ***sopor*** and use one of its functions

```python
import sopor

# Getting a list of all stations
station_list = sopor.get_station_list()

# Getting services of a station, here station 901006.
services = sopor.get_station_info("901006", "2085")
```
