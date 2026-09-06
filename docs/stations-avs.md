# Recycling Stations (ÅVS – Återvinningsstationer) API

Recycling stations (*återvinningsstationer* or *ÅVS*) are the unstaffed neighborhood recycling drop-off points located on public land across Sweden, primarily providing containers for household packaging (paper, plastic, metal, glass, newspaper, batteries, and textiles).

---

## Endpoints

### 1. Get All Stations (`GetAllAVS`)

Retrieves the nationwide list of active recycling stations.

- **Method**: `GET`
- **URL**: `https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/GetAllAVS`
- **Authentication**: None
- **Parameters**: None

#### Response Structure (`200 OK`)
Returns a JSON array of station objects:

```json
[
  {
    "id": "8e4d3db1-983c-48a4-a3e9-5849c7ba0b2b",
    "accountId": "bd66b3f5-7b21-4f08-986a-25f91e4be77f",
    "apiVersion": "1.0.0",
    "externalAvsId": "11045",
    "name": "Glädjens ÅVS",
    "secondaryName": null,
    "propertyNumber": "GLÄDJEN 1:1",
    "municipalityCode": "0114",
    "streetAddress": "Frejavägen",
    "lat": "59.513491498998114",
    "long": "17.930354788447218",
    "extraInfo": null,
    "services": null
  }
]
```

#### Field Reference
| Field | Type | Description |
|---|---|---|
| `id` | `string (UUID)` | Internal unique identifier for the station in Avfallshubben |
| `accountId` | `string (UUID)` | Identifier of the municipal authority or contractor managing the station |
| `apiVersion` | `string` | Ingestion source format (`1.0.0` via API, or `Excel` via manual upload) |
| `externalAvsId` | `string` | The public station identifier (historically assigned by FTI AB) |
| `name` | `string` | Primary station name (often a landmark, square, or street name) |
| `secondaryName` | `string` | Optional descriptive subtitle or location hint |
| `propertyNumber` | `string` | Real estate / cadastre property designation (*fastighetsbeteckning*) |
| `municipalityCode` | `string` | 4-digit Swedish municipality code (*kommunkod*, e.g. `0114` for Upplands Väsby) |
| `streetAddress` | `string` | Street address or road description |
| `lat`, `long` | `string (float)` | WGS84 geographic coordinates |
| `extraInfo` | `string` | Public guidance (e.g. temporary relocation, roadwork notice) |
| `services` | `null` | In `GetAllAVS`, this is null; use `GetAVS` to fetch service details |

---

### 2. Get Station Details & Service Info (`GetAVS`)

Retrieves detailed information and container servicing schedules for a specific station.

- **Method**: `GET`
- **URL**: `https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/GetAVS`
- **Authentication**: None
- **Query Parameters**:
  - `externalAvsId` *(required, string)*: The station ID (e.g. `11045`)
  - `municipalityCode` *(required, string)*: The 4-digit municipality code (e.g. `0114`)

#### Example Request
```bash
curl -G "https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/GetAVS" \
  --data-urlencode "externalAvsId=11045" \
  --data-urlencode "municipalityCode=0114"
```

#### Response Structure (`200 OK`)
```json
{
  "avs": {
    "id": "8e4d3db1-983c-48a4-a3e9-5849c7ba0b2b",
    "accountId": "bd66b3f5-7b21-4f08-986a-25f91e4be77f",
    "apiVersion": "Excel",
    "externalAvsId": "11045",
    "name": "Glädjens ÅVS",
    "secondaryName": "",
    "propertyNumber": "",
    "municipalityCode": "0114",
    "streetAddress": "Frejavägen",
    "lat": "59.513491498998114",
    "long": "17.930354788447218",
    "extraInfo": "",
    "services": [
      {
        "id": "13f3b823-fe35-468d-b75b-10f4b3f32f39",
        "avsId": "8e4d3db1-983c-48a4-a3e9-5849c7ba0b2b",
        "externalAvsId": "11045",
        "municipalityCode": "0114",
        "serviceId": "101",
        "serviceType": 1,
        "lastAction": null,
        "lastActionAltText": "",
        "nextAction": null,
        "nextActionAltText": "Töms måndag , torsdag och lördag",
        "extraInfo": "",
        "numberOfServices": 1,
        "responsible": "SÖRAB/Strandqvist"
      }
    ]
  },
  "disableServiceRequestReportingToUser": false,
  "disableServiceRequestErrorDescriptionForUser": false,
  "enableServiceRequestImagePath": true,
  "customServiceRequestUrl": ""
}
```

#### Top-level Control Flags
- `disableServiceRequestReportingToUser` (`bool`): When `true`, citizen fault reporting (*felanmälan*) is disabled on `sopor.nu`.
- `disableServiceRequestErrorDescriptionForUser` (`bool`): When `true`, free-text description in reports is prohibited.
- `enableServiceRequestImagePath` (`bool`): When `true`, photo upload is accepted in citizen reports.
- `customServiceRequestUrl` (`string`): If the municipality uses its own reporting portal, this field contains the redirect URL.

#### Services Array Item Reference
| Field | Type | Description |
|---|---|---|
| `serviceId` | `string` | Category/service identifier code (e.g. `101`, `102`) |
| `serviceType` | `integer` | Numerical fraction/service type identifier (1–10) |
| `lastAction` | `string (ISO 8601)` | Timestamp of previous recorded emptying or cleaning |
| `lastActionAltText` | `string` | Optional human-readable description of the last action |
| `nextAction` | `string (ISO 8601)` | Projected timestamp of the next emptying/cleaning |
| `nextActionAltText` | `string` | Human-readable schedule (e.g. `"Töms måndag, torsdag och lördag"`) |
| `numberOfServices` | `integer` | Number of containers for this fraction installed at the station |
| `responsible` | `string` | Name of the operating contractor or municipal company |

#### Standard `serviceType` & `serviceId` Mapping
| `serviceType` | Standard `serviceId` | Swedish Name | English Description |
|---|---|---|---|
| `1` | `101` | Pappersförpackningar | Paper & cardboard packaging |
| `2` | `102` | Plastförpackningar | Plastic packaging |
| `3` | `103` | Metallförpackningar | Metal packaging |
| `4` | `104` | Ofärgade glasförpackningar | Clear glass packaging |
| `5` | `105` | Färgade glasförpackningar | Coloured glass packaging |
| `6` | `106` | Tidningar & trycksaker | Newspapers & periodicals |
| `7` | `107` | Batterier | Battery collection box |
| `8` | `108` | Textil | Textile collection |
| `9` | `109` | Städning | Site cleaning & litter clearance |
| `10` | `110` | Snöröjning / Halkbekämpning | Winter maintenance (plowing / gritting) |

---

### 3. Unified Geo Cache Feed (`GetCacheItems`)

Used by the `sopor.nu` map interface to fetch all map markers (both ÅVS stations and ÅVC centers) in a single compressed payload.

- **Method**: `GET`
- **URL**: `https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/GetCacheItems/`
- **Authentication**: None

#### Response Structure (`200 OK`)
```json
{
  "avsList": [
    {
      "id": "8e4d3db1-983c-48a4-a3e9-5849c7ba0b2b",
      "externalAvsId": "11045",
      "name": "Glädjens ÅVS",
      "streetAddress": "Frejavägen",
      "municipalityCode": "0114",
      "lat": "59.513491498998114",
      "long": "17.930354788447218",
      "extraInfo": ""
    }
  ],
  "avcList": [
    {
      "externalAvcId": "246301",
      "name": "Åsele Återvinningscentral",
      "streetAddress": "Industrivägen 15",
      "municipalityCode": "2463",
      "lat": "64.176375",
      "long": "17.367202",
      "openingHours": "Tisdagar 12.00-18:30\r\nTorsdagar 09:00-16:00"
    }
  ]
}
```

---

### 4. Municipal Station Selector (`GetByMuicipalityCode`)

Generates HTML dropdown options for stations within a specific municipality.

- **Method**: `GET`
- **URL**: `https://www.sopor.nu/umbraco/surface/AvfallshubbenSurface/GetByMuicipalityCode/`
- **Query Parameter**: `municipalityCode` (e.g. `0114`)

#### Example Response
```html
<select class="form-control js-choice1 w-100 mb-3" name="avs">
    <option selected disabled value="">Välj station</option>
    <option class="avs-option" data-type="avs" value="11045:0114:0:0">Glädjens ÅVS (11045)</option>
</select>
```
The option value format is: `{externalAvsId}:{municipalityCode}:{isAvc}:{hasCustomUrl}`.
