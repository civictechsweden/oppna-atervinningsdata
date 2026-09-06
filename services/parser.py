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

        stations = sorted(stations, key=lambda x: (x["municipalityCode"], x["id"]))
        return stations

    @staticmethod
    def parse_station_info(response):
        if isinstance(response, tuple):
            id_pair, data = response
        else:
            id_pair, data = None, response

        if not isinstance(data, dict):
            return {"id_pair": id_pair, "services": None, "error": True}

        avs = data.get("avs")
        if not avs:
            return {"id_pair": id_pair, "services": None, "error": True}

        if id_pair is None:
            id_pair = (avs.get("externalAvsId"), avs.get("municipalityCode"))

        raw_services = avs.get("services")
        if raw_services is None:
            return {"id_pair": id_pair, "services": [], "error": False}

        clean_services = []
        for service in raw_services:
            clean = {k: v for k, v in service.items() if k not in ("id", "avsId")}
            clean_services.append(clean)

        clean_services.sort(key=lambda x: x.get("serviceId", 0))

        return {
            "id_pair": id_pair,
            "services": clean_services,
            "error": False,
        }
    @staticmethod
    def parse_stations_info(responses):
        return list(map(Parser.parse_station_info, responses))
