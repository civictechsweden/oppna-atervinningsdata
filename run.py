import copy

from services.writer import Writer

import ftiab

stations = ftiab.get_station_list()
#stations = ftiab.get_station_list_from_file()

print('Writing station list...')

Writer.write_json(stations, 'data/stations.json')
Writer.write_csv(stations, 'data/stations.csv')

station_ids = [station['id'] for station in stations]

stations_info = ftiab.get_stations_maintenance_info(station_ids)
#stations_info = ftiab.get_stations_maintenance_info_from_files()

for station_info in stations_info:
    id = station_info["id"]

    try:
        station = next((s for s in stations if s['id'] == id), None)
        station['maintenance'] = station_info['categories']
    except TypeError:
        print(f'TypeError for station {id}')

    print(f'Writing maintenance info and history for station {id}...')

    Writer.write_json(station_info['categories'], f'data/stationMaintenance/{id}.json')
    Writer.write_csv(station_info['categories'], f'data/stationMaintenance/{id}.csv')

    categories = [copy.deepcopy(category) for category in station_info['categories'] if category['senaktivitet']]

    if not categories:
        continue

    for category in categories:
        category['maintenance'] = category['senaktivitet']
        del category['senaktivitet']
        del category['nastaaktivitet']

Writer.write_json(stations, 'data/stations_with_maintenance.json')
