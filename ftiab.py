from services.downloader import Downloader
from services.parser import Parser

def get_station_list(downloader=Downloader()):
    return Parser.parse_station_list(downloader.fetch_station_list())

def get_station_maintenance_info(id, downloader=Downloader()):
    return Parser.parse_station_maintenance_info(downloader.fetch_station_maintenance_info(id).result().content)

def get_stations_maintenance_info(ids, downloader=Downloader()):
    return Parser.parse_stations_maintenance_info(downloader.fetch_stations_maintenance_info(ids))
