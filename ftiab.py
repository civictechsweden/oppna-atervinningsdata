import os, json

from services.downloader import Downloader
from services.parser import Parser

def get_station_list(downloader=Downloader()):
    return Parser.parse_station_list(downloader.fetch_station_list())

def get_station_list_from_file():
    with open(f'data/stations.json') as file_json:
        station_list = json.load(file_json)
    return station_list

def get_station_maintenance_info(id, downloader=Downloader()):
    return Parser.parse_station_maintenance_info(downloader.fetch_station_maintenance_info(id).result().content)

def get_stations_maintenance_info(ids, downloader=Downloader()):
    return Parser.parse_stations_maintenance_info(downloader.fetch_stations_maintenance_info(ids))

def get_stations_maintenance_info_from_files():
    stations_info = []

    for file in os.listdir('data/stationMaintenance'):
        if '.json' in file:
            with open(f'data/stationMaintenance/{file}') as file_json:
                categories = json.load(file_json)
            stations_info.append(
                {
                    'id': file.replace('.json', ''),
                    'categories': categories
                }
            )

    return stations_info
