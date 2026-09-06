# Sopor.nu & Avfallshubben Public API Documentation

This directory documents the public, unauthenticated APIs powering **[sopor.nu](https://www.sopor.nu)** and backed by **Avfall Sverige's Avfallshubben** (`https://avfallshubben.avfallsverige.se`).

These APIs drive the citizen-facing web frontend—allowing people to find Swedish recycling stations and centers, check container emptying schedules, submit maintenance reports, and look up waste sorting rules.

---

## Official OpenAPI / Swagger Specifications

Avfall Sverige hosts an OpenAPI 3.0 specification for Avfallshubben:

- **Swagger UI**: [https://avfallshubben.avfallsverige.se/swagger/index.html](https://avfallshubben.avfallsverige.se/swagger/index.html)
- **OpenAPI 3.0 JSON**: [https://avfallshubben.avfallsverige.se/swagger/v1/swagger.json](https://avfallshubben.avfallsverige.se/swagger/v1/swagger.json)

> **Note on Authentication**: The `/api/avs/*` endpoints documented in Swagger are protected by municipal API keys (HTTP 401 Unauthorized) for contractors and municipal authorities to manage their stations. However, the Umbraco API endpoints (`/umbraco/Api/SoporApi/*`) and Surface Controllers (`/umbraco/surface/*`) used by `sopor.nu` are **publicly accessible without authentication**.

---

## Base URLs

| Service | Base URL | Purpose |
| --- | --- | --- |
| **Avfallshubben API** | `https://avfallshubben.avfallsverige.se` | Primary REST API for station data, centers, and cache feeds |
| **Sopor.nu Web Portal** | `https://www.sopor.nu` | Surface controllers, autocomplete, and sorting guide queries |

---

## Documentation Index

1. **[Recycling Stations (ÅVS – Återvinningsstationer)](stations-avs.md)**
   - Unstaffed neighborhood packaging collection stations (paper, plastic, metal, glass, newspapers, batteries).
   - Endpoints: `GetAllAVS`, `GetAVS`, `GetCacheItems`, `GetByMuicipalityCode`.
   - Schedules for emptying, cleaning, and contractor responsibilities.

2. **[Recycling Centers (ÅVC – Återvinningscentraler)](centers-avc.md)**
   - Staffed municipal recycling centers for bulky items, electronics, hazardous waste, garden waste, etc.
   - Endpoints: `GetAllAVC`, `GetAVC`, `AvfallshubbenSurface/GetAvc`.
   - Opening hours, visit quotas (`noOfFreeEntries`), entry systems, and accepted waste fractions (`fractionIds`).

3. **[Citizen Issue Reporting / Felanmälan](issue-reporting.md)**
   - How citizens report full containers, scattered litter, or icy/snowy stations.
   - Endpoint: `POST /umbraco/surface/avssurface/SubmitServiceRequest`.
   - Taxonomy of service codes (`needsEmptying`, `needsCleaning`, `winterManagement`).

4. **[Waste Sorting Guide (Sorteringsguide)](sorting-guide.md)**
   - National directory of 1,199 consumer items mapped to disposal fractions.
   - Endpoints: `AutocompleteApi/GetStrings` and sorting guide queries.
