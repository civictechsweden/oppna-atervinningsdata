import copy
import json
import os
from services.writer import Writer

import sopor

existing_stations_file = "data/stations_with_services.json"
existing_stations_by_id = {}
if os.path.exists(existing_stations_file):
    try:
        with open(existing_stations_file, "r") as f:
            for s in json.load(f):
                existing_stations_by_id[sopor.id_pair(s)] = s
    except Exception as e:
        print(f"Could not load existing stations: {e}")

stations = sopor.get_station_list()
print(f"Fetched {len(stations)} stations.")

if existing_stations_by_id and len(stations) < len(existing_stations_by_id) * 0.8:
    raise RuntimeError(
        f"ABORTING: Station count dropped from {len(existing_stations_by_id)} to {len(stations)} "
        f"({len(existing_stations_by_id) - len(stations)} stations missing upstream). "
        f"Aborting run to protect dataset from corruption."
    )

print("Writing station list...")
Writer.write_json(stations, "data/stations.json")
Writer.write_csv(stations, "data/stations.csv")

station_id_pairs = [(s["id"], s["municipalityCode"]) for s in stations]

stations_info = sopor.get_stations_info(station_id_pairs)

services = []

for station_info in stations_info:
    id_pair = station_info["id_pair"]

    if station_info.get("error") or station_info.get("services") is None:
        print(f"Warning: Failed or invalid service data for station {id_pair}")
        prev_station = existing_stations_by_id.get(id_pair)
        if prev_station and "services" in prev_station:
            station_info["services"] = copy.deepcopy(prev_station["services"])
            print(f"  Preserved previous services for station {id_pair}")
        else:
            station_info["services"] = []

    services.extend(copy.deepcopy(station_info["services"]))

    for service in station_info["services"]:
        service.pop("externalAvsId", None)
        service.pop("municipalityCode", None)

    station = next((s for s in stations if sopor.id_pair(s) == id_pair), None)
    if station is not None:
        station["services"] = station_info["services"]

print("Writing service list...")
Writer.write_csv(services, "data/services.csv")

print("Writing station list with services...")
Writer.write_json(stations, "data/stations_with_services.json")
