from bs4 import BeautifulSoup

class Parser(object):
    @staticmethod
    def parse_station_list(response):
        print('Parsing all stations...')

        soup = BeautifulSoup(response, 'lxml')

        stations = []

        for avs in soup.select('getavsresult > avs'):
            station = {}

            for child in avs.children:
                key = child.name
                value = child.text

                if key == 'avsid':
                    station['id'] = value
                elif key != 'latitud' and key != 'longitud':
                    station[child.name.replace('decimal', 'e')] = child.text

            stations.append(station)

        print('Finished parsing all stations.')

        return stations

    @staticmethod
    def parse_station_maintenance_info(response):

        soup = BeautifulSoup(response, 'lxml')

        try:
            id = int(soup.select_one('getavsstatistikresult > avsstatistik > avsid').text)
        except AttributeError:
            print(soup)

        print(f"Parsing maintenance for station {id}...")

        maintenance = []

        for avs in soup.select('getavsstatistikresult > avsstatistik'):
            statistic = {}

            for child in avs.children:
                if child.name != 'avsid':
                    statistic[child.name] = child.text if child.text != '1900-01-01T00:00:00' else None

            maintenance.append(statistic)

        return {
            'id': id,
            'categories': maintenance
        }

    @staticmethod
    def parse_stations_maintenance_info(responses):
        return list(map(Parser.parse_station_maintenance_info, responses))

