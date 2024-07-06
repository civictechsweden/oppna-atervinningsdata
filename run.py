import copy
from services.writer import Writer

import sopor

stations = sopor.get_station_list()
# stations = sopor.get_station_list_from_file()

print("Writing station list...")
Writer.write_json(stations, "data/stations.json")
Writer.write_csv(stations, "data/stations.csv")

station_id_pairs = [(s["id"], s["municipalityCode"]) for s in stations]

stations_info = sopor.get_stations_info(station_id_pairs)
# stations_info = sopor.get_stations_info_from_files()

services = []

for station_info in stations_info:
    services.extend(copy.deepcopy(station_info["services"]))

    id_pair = station_info["id_pair"]

    try:
        for service in station_info["services"]:
            del service["externalAvsId"]
            del service["municipalityCode"]

        station = next((s for s in stations if sopor.id_pair(s) == id_pair), None)
        station["services"] = station_info["services"]
    except TypeError as e:
        print(f"TypeError for station {id_pair}: {e}")

print("Writing service list...")
Writer.write_csv(services, "data/services.csv")

print("Writing station list with services...")
Writer.write_json(stations, "data/stations_with_services.json")
