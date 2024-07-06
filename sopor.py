import json

from services.downloader import Downloader
from services.parser import Parser


def id_pair(station):
    return (station["id"], station["municipalityCode"])


def get_station_list(downloader=Downloader()):
    return Parser.parse_station_list(downloader.fetch_station_list())


def get_station_list_from_file():
    with open("data/stations.json") as file_json:
        stations = json.load(file_json)
    return stations


def get_station_info(id_pair, downloader=Downloader()):
    return Parser.parse_station_info(
        downloader.fetch_station_info(id_pair).result().json()
    )


def get_stations_info(id_pairs, downloader=Downloader()):
    return Parser.parse_stations_info(downloader.fetch_stations_info(id_pairs))


def get_stations_info_from_files():
    with open("data/stations_with_services.json") as file_json:
        stations = json.load(file_json)

    return [{"id_pair": id_pair(s), "services": s["services"]} for s in stations]
