# Öppna återvinningsdata (Open recycling data)

This python script can automatically fetch all the Swedish recycling stations (återvinningsstationer) using FTI AB's open APIs. It also fetches the station "maintenance info", which means the last and next time the station is cleaned and various containers emptied.

It exports the result as JSON or CSV in the data folder. The history of the maintenance tasks is also recorded in CSV files.

On this repository, you can download the data directly. It is updated monthly by Github Actions every night at 1AM CET.

The data is updated continuously by FTI AB. The data made available by this hobby project might be outdated, or inaccurate.

License for the code is AGPL 3.0, license for the data is CC0 (but attribution is appreciated).

## Why?

The list of recycling stations often comes up among the most requested datasets in Sweden. Although the information is well structured and made available nationally through open APIs and a user-friendly map by FTI AB, it is not available as open data.

And since they aren't public sector, no one has actually asked FTI AB if they could publish the list.

Therefore, introducing Öppna återvinningsdata. And I started a dialogue with FTI AB to see if they could publish themselves, how the data should be licensed and if it can be published on Sweden's national data portal.

## Installation

- Install Python 3 on your machine if you don't already have it.

- Install the dependencies

```python
pip install -r requirements.txt
```

## Usage

- Import ***ftiab*** and use one of its functions

```python
import ftiab

# Getting a list of all planes in the register
station_list = ftiab.get_station_list()

# Getting maintenance info of a station, here station 1.
maintenance_info = ftiab.get_station_maintenance_info('1')

# Getting a list with the details of all planes in the register
all_stations_maintenance_info = fti.get_stations_maintenance_info()
```
