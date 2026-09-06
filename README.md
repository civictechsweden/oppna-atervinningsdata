# Öppna återvinningsdata (Open Recycling Data)

**Öppna återvinningsdata** is a civic tech project to provide open data about Swedish recycling stations (*återvinningsstationer*, ÅVS) and staffed municipal recycling centers (*återvinningscentraler*, ÅVC). Between 2022 and 2026, the project was scraping and parsing data using a script (i.e. downloading it programmatically but using an unofficial method for lack of a better one) and republishing it to allow for more people to reuse it. Since the latest efforts to publish an open API with a public specification, I have decided to archive the project, stop the automatic republishing and instead use this repository to document the official API. You can read more about the history of the project [below](#project-history--background).

The Swedish national waste platform—**Avfallshubben** (`https://avfallshubben.avfallsverige.se`), managed by **Avfall Sverige** and powering the citizen portal **[sopor.nu](https://www.sopor.nu)**—exposes an official OpenAPI 3.0 / Swagger specification:

- **Swagger UI**: [https://avfallshubben.avfallsverige.se/swagger/index.html](https://avfallshubben.avfallsverige.se/swagger/index.html)
- **OpenAPI 3.0 JSON**: [https://avfallshubben.avfallsverige.se/swagger/v1/swagger.json](https://avfallshubben.avfallsverige.se/swagger/v1/swagger.json)

While Avfall Sverige treats Avfallshubben as an internal administrative tool for municipalities and does not publish it as open data on [dataportal.se](https://www.dataportal.se), the underlying citizen-facing REST endpoints are public and unauthenticated. This repository provides comprehensive documentation for these endpoints in the [`docs/`](docs/) directory.

---

## API Documentation (`docs/`)

Explore the detailed documentation for the public APIs powering `sopor.nu`:

- **[API Overview & Architecture](docs/README.md)**: Base URLs, architecture, authentication notes, and Swagger details.
- **[Recycling Stations (ÅVS)](docs/stations-avs.md)**: National station directory (`GetAllAVS`), container emptying schedules, contractor assignments, and cache feeds (`GetAVS`, `GetCacheItems`).
- **[Recycling Centers (ÅVC)](docs/centers-avc.md)**: Staffed municipal centers (`GetAllAVC`, `GetAVC`), opening hours text, visitor quotas (`noOfFreeEntries`), entry systems, and accepted waste fractions (`fractionIds`).
- **[Citizen Issue Reporting / Felanmälan](docs/issue-reporting.md)**: Taxonomy of problem codes for reporting full containers (`needsEmptying`), illegal dumping (`needsCleaning`), or snow/ice hazards (`winterManagement`).
- **[National Sorting Guide / Sorteringsguide](docs/sorting-guide.md)**: Public dictionary of 1,199 consumer items (`AutocompleteApi/GetStrings`) and how they map to disposal fractions.

---

## Project History & Background

### Why this project started (FTI AB Era, 2022–2023)

The directory of Swedish recycling stations has consistently been one of the most requested public datasets in Sweden. Historically, packaging collection was run by the private producer consortium **FTI AB** (*Förpacknings- och tidningsinsamlingen*). While FTI provided a website and SOAP service (`ftiws.ftiab.se`), the data was very hard to reuse and was not released under an open data license. This project was launched to bridge that gap by converting SOAP XML into open CSV and JSON files under CC0.

### The Avfallshubben Transition (July 2024)

Under Sweden's Packaging Reform (*Förordning 2022:1274 om producentansvar för förpackningar*), responsibility for packaging collection was transferred to Sweden's 290 municipalities on **January 1, 2024**. Avfall Sverige developed **Avfallshubben** to replace FTI's backend. In July 2024, this repository was migrated to consume the new REST endpoints on `avfallshubben.avfallsverige.se` (`GetAllAVS` and `GetAVS`).

### Transition to Open Documentation (September 2026)

In autumn 2025, Avfall Sverige expanded the platform with staffed recycling centers (ÅVC) and an OpenAPI standard. However, Avfall Sverige does not offer an official documentation nor does it index the APIs on [dataportal.se](https://www.dataportal.se)

---

## Historical Data

Outdated data files remain available in the [`data/`](data/) directory:

- `data/stations.json` / `data/stations.csv`: Registry of ~4,750 recycling stations with coordinates and cadastral references.
- `data/services.csv`: Flattened container services, emptying frequencies, and operating contractors.
- `data/stations_with_services.json`: Combined hierarchical JSON of stations with nested container services.

---

## Running the Code

### 1. Prerequisites

Install [uv](https://docs.astral.sh/uv/) (Python package and project manager) and Python 3.14:

```bash
# Install dependencies from pyproject.toml / uv.lock
uv sync
```

### 2. Running the Full Scraper

To run the scraper manually against Avfallshubben:

```bash
uv run run.py
```

The script will:

1. Load existing stations from `data/stations_with_services.json`.
2. Fetch the latest station list via `GetAllAVS`.
3. Concurrently fetch container service details for each station with retry backoff and timeout handling.
4. Export updated records to `data/stations.json`, `data/stations.csv`, `data/services.csv`, and `data/stations_with_services.json`.

### 3. Programmatic Usage in Python

You can import the `sopor` module directly:

```python
import sopor

# Fetch list of all active stations
stations = sopor.get_station_list()
print(f"Fetched {len(stations)} stations")

# Fetch detailed container services for a specific station (e.g. ID 11045 in Upplands Väsby)
service_info = sopor.get_station_info(("11045", "0114"))
print("Station services:", service_info)
```

---

## License

- **Code** (scraper, parser, utilities): [AGPL 3.0](LICENSE)
- **Data & Documentation**: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (Attribution appreciated)
