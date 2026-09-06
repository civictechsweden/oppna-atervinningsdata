# Sopor.nu & Avfallshubben Public API Documentation

This directory documents the public, unauthenticated APIs powering **[sopor.nu](https://www.sopor.nu)** and backed by **Avfall Sverige's Avfallshubben** (`https://avfallshubben.avfallsverige.se`).

These APIs drive the citizen-facing web frontend—allowing people to find Swedish recycling stations and centers, check container emptying schedules, submit maintenance reports, and look up waste sorting rules.

---

## Official OpenAPI / Swagger Specifications

Avfall Sverige hosts an OpenAPI 3.0 specification for Avfallshubben:

- **Swagger UI**: [https://avfallshubben.avfallsverige.se/swagger/index.html](https://avfallshubben.avfallsverige.se/swagger/index.html)
- **OpenAPI 3.0 JSON**: [https://avfallshubben.avfallsverige.se/swagger/v1/swagger.json](https://avfallshubben.avfallsverige.se/swagger/v1/swagger.json)

### How to convert Swagger endpoints to the public unauthenticated endpoints

The Swagger specification at `/swagger/v1/swagger.json` documents the exact underlying data models (`Avs`, `Service`, `ServiceCategory`), but uses the authenticated `/api/avs/*` route prefix intended for suppliers.

To convert any documented read endpoint to its public, unauthenticated equivalent used by `sopor.nu`:

1. **Replace the route prefix**:
   Change `/api/avs/` (or `/api/v1-1-0/avs/`) to `/umbraco/Api/SoporApi/`
2. **Capitalize the acronym**:
   - `/api/avs/GetAllAvs` $\rightarrow$ `/umbraco/Api/SoporApi/GetAllAVS`
   - `/api/avs/GetAvs` $\rightarrow$ `/umbraco/Api/SoporApi/GetAVS`
   - For recycling centers: `GetAllAVC` and `GetAVC`
3. **Query parameters and response schemas are identical**:
   The query parameters (`externalAvsId`, `municipalityCode`) and response objects match the `Avs` and `Service` schemas documented in Swagger.

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
