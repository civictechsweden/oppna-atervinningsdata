from bs4 import BeautifulSoup
import json


class Parser(object):

    @staticmethod
    def parse_station_list(response):
        print("Parsing all stations...")

        stations = []

        for item in response:
            station = {"id": item["externalAvsId"]}

            for key in [
                "name",
                "secondaryName",
                "propertyNumber",
                "streetAddress",
                "municipalityCode",
                "extraInfo",
            ]:
                station[key] = item[key]

            station["latitude"] = float(item["lat"])
            station["longitude"] = float(item["long"])

            stations.append(station)

        return stations

    @staticmethod
    def parse_station_info(response):

        services = response["avs"]["services"]

        clean_services = []
        for service in services:
            del service["id"]
            del service["avsId"]
            clean_services.append(service)

        return {
            "id_pair": (
                response["avs"]["externalAvsId"],
                response["avs"]["municipalityCode"],
            ),
            "services": clean_services,
        }

    @staticmethod
    def parse_stations_info(responses):
        return list(map(Parser.parse_station_info, responses))
