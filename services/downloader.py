from concurrent.futures import as_completed
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from urllib3.util import Retry

FTIWS_URL = 'https://ftiws.ftiab.se/fti_ws/fti_ws.asmx?op={}'

def soap_envelope(query, xml_parameters):
    return f"""<?xml version="1.0" encoding="utf-8"?>
              <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
                  <soap12:Body>
                      <{query} xmlns="http://tempuri.org/">
                          {xml_parameters}
                      </{query}>
                  </soap12:Body>
              </soap12:Envelope>"""

class Downloader(object):

    def __init__(self):
        adapter = HTTPAdapter(max_retries=Retry(total=10, backoff_factor=0.1))

        self.s = FuturesSession(max_workers=100)
        self.s.mount('https://', adapter)
        self.s.headers = {'Content-Type': 'text/xml;charset=UTF-8'}

    def fetch_station_list(self):
        print(f'Fetching all stations...')

        soap_query = 'GetAVS'
        data = soap_envelope(soap_query, '<sLan/><sKommun/><lAVSid>0</lAVSid>')

        future = self.s.post(FTIWS_URL.format(soap_query), data=data)

        return future.result().content

    def fetch_station_maintenance_info(self, id):
        print(f'Fetching maintenance data for station {id}...')

        soap_query = 'GetAVSStatistik'
        data = soap_envelope(soap_query, f'<lAvsId>{id}</lAvsId>')

        future = self.s.post(FTIWS_URL.format(soap_query), data=data)

        future.id = id
        return future

    def fetch_stations_maintenance_info(self, ids):
        futures = [self.fetch_station_maintenance_info(id) for id in ids]

        i = 0
        for future in as_completed(futures):
            i += 1
            print(f'Fetched maintenance data for station {future.id} ({i}/{len(futures)})')

        return [future.result().content for future in futures]
