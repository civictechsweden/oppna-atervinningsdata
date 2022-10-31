import datetime as dt
import pandas as pd

from services.writer import Writer

import ftiab

stations = ftiab.get_station_list()

Writer.write_json(stations, 'data/stations.json')
Writer.write_csv(stations, 'data/stations.csv')

station_ids = [station['id'] for station in stations]

stations_info = ftiab.get_stations_maintenance_info(station_ids)[:10]

for station_info in stations_info:
    id = station_info["id"]

    Writer.write_json(station_info['categories'], f'data/stationMaintenance/{id}.json')
    Writer.write_csv(station_info['categories'], f'data/stationMaintenance/{id}.csv')

    categories = [category for category in station_info['categories'] if category['senaktivitet']]
    for category in categories:
        category['maintenance'] = category['senaktivitet']
        del category['senaktivitet']
        del category['nastaaktivitet']

    try:
        maintenance_history = pd.read_csv(f'data/stationMaintenanceHistory/{id}.csv')
    except FileNotFoundError:
        maintenance_history = pd.DataFrame.from_dict(categories)
        maintenance_history.to_csv(f'data/stationMaintenanceHistory/{id}.csv', index=False)
        continue

    for category in categories:
        latest_maintenance = maintenance_history.query(f"materialid == {category['materialid']}").tail(1)
        new_maintenance = pd.DataFrame(category, index=[0])

        def date_for(df):
            return dt.datetime.strptime(df['maintenance'].iloc[0], '%Y-%m-%dT%H:%M:%S')

        if date_for(new_maintenance) > date_for(latest_maintenance):
            maintenance_history = pd.concat([maintenance_history, new_maintenance])
            maintenance_history.to_csv(f'data/stationMaintenanceHistory/{id}.csv', index=False)


