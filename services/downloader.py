from concurrent.futures import as_completed
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from urllib3.util import Retry

SOPOR_URL = "https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/"


class Downloader(object):

    def __init__(self):
        self.s = FuturesSession(max_workers=10)
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.s.mount("https://", adapter)
        self.s.mount("http://", adapter)
    def fetch_station_list(self):
        print("Fetching all stations...")
        resp = self.s.get(SOPOR_URL + "GetAllAVS", timeout=30).result()
        resp.raise_for_status()
        return resp.json()

    def fetch_station_info(self, id_pair):
        avs_id, municipality_code = id_pair
        params = {"externalAvsId": avs_id, "municipalityCode": municipality_code}
        future = self.s.get(SOPOR_URL + "GetAVS", params=params, timeout=15)
        future.id = avs_id
        future.id_pair = id_pair
        return future

    def fetch_stations_info(self, id_pairs):
        futures = [self.fetch_station_info(id_pair) for id_pair in id_pairs]

        i = 0
        for future in as_completed(futures):
            i += 1
            print(f"Fetched service data for station {future.id} ({i}/{len(futures)})")

        results = []
        for future in futures:
            try:
                resp = future.result()
                if resp.ok:
                    data = resp.json()
                    # Ensure id_pair is attached if response is missing it
                    results.append((future.id_pair, data))
                else:
                    print(f"Error fetching station {future.id}: HTTP {resp.status_code}")
                    results.append((future.id_pair, {"avs": None, "error": f"HTTP {resp.status_code}"}))
            except Exception as e:
                print(f"Exception fetching station {future.id}: {e}")
                results.append((future.id_pair, {"avs": None, "error": str(e)}))
        return results
