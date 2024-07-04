import copy

from services.writer import Writer

import sopor

stations = sopor.get_station_list()
# stations = sopor.get_station_list_from_file()

print("Writing station list...")
Writer.write_json(stations, "data/stations.json")
Writer.write_csv(stations, "data/stations.csv")

station_id_pairs = [
    (station["id"], station["municipalityCode"]) for station in stations
]

stations_info = sopor.get_stations_info(station_id_pairs)
# stations_info = sopor.get_stations_info_from_files()

for station_info in stations_info:
    id_pair = station_info["id_pair"]

    try:
        station = next((s for s in stations if sopor.id_pair(s) == id_pair), None)
        station["services"] = station_info["services"]
    except TypeError:
        print(f"TypeError for station {id}")

print("Writing station list with services...")
Writer.write_json(stations, "data/stations_with_services.json")
