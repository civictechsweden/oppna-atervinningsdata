from concurrent.futures import as_completed
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from ssl import create_default_context, Purpose
from urllib3.util import Retry

SOPOR_URL = "https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/"


class Downloader(object):

    def __init__(self):
        self.s = FuturesSession(max_workers=10)

    def fetch_station_list(self):
        print("Fetching all stations...")
        future = self.s.get(SOPOR_URL + "GetAllAVS")

        return future.result().json()

    def fetch_station_info(self, id_pair):
        avs_id, municipality_code = id_pair
        print(f"Fetching service data for station {avs_id}...")

        params = {"externalAvsId": avs_id, "municipalityCode": municipality_code}
        future = self.s.get(SOPOR_URL + "GetAVS", params=params)

        future.id = avs_id
        return future

    def fetch_stations_info(self, id_pairs):
        futures = [self.fetch_station_info(id_pair) for id_pair in id_pairs]

        i = 0
        for future in as_completed(futures):
            i += 1
            print(f"Fetched service data for station {future.id} ({i}/{len(futures)})")

        return [future.result().json() for future in futures]
