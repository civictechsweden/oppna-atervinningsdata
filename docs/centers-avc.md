# Recycling Centers (ÅVC – Återvinningscentraler) API

Recycling centers (*återvinningscentraler* or *ÅVC*) are staffed municipal waste management facilities in Sweden. Unlike unstaffed neighborhood packaging stations (ÅVS), recycling centers accept bulk waste, hazardous materials, electronics, scrap metal, demolition debris, garden waste, and items for reuse.

---

## Endpoints

### 1. Get All Recycling Centers (`GetAllAVC`)

Retrieves the nationwide list of registered municipal recycling centers.

- **Method**: `GET`
- **URL**: `https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/GetAllAVC`
- **Authentication**: None
- **Parameters**: None

#### Response Structure (`200 OK`)
Returns an array of ÅVC objects:

```json
[
  {
    "id": "040ffe38-82e3-4dde-a356-c46e5fba566a",
    "accountId": "6996e0b9-dc33-49f6-b964-f749c014cc46",
    "name": "Åsele Återvinningscentral",
    "externalAvcId": "246301",
    "propertynumber": "Åsele",
    "secondaryName": null,
    "municipalityCode": "2463",
    "lat": "64.176375",
    "long": "17.367202",
    "openingHours": "Tisdagar 12.00-18:30\r\nTorsdagar 09:00-16:00",
    "openingHoursUrl": "https://www.sav.nu/media/3ecfmoew/klar-7.png",
    "noOfFreeEntries": null,
    "entrySystem": null,
    "proffessionalInfo": null,
    "streetAddress": "Industrivägen 15",
    "zipCode": "97931",
    "city": "Åsele",
    "contactEmail": "kundtjanstsav@sav.nu",
    "contactPhone": "09411400",
    "extraInfo": null,
    "url": "WWW.SAV.NU",
    "fractionIds": "2019,2021,2017,2013,2030,2023,2020,2022,2025,2015,2026,2032"
  }
]
```

---

### 2. Get Center Details (`GetAVC`)

Retrieves detailed access rules, contact info, and accepted materials for a specific recycling center.

- **Method**: `GET`
- **URLs**:
  - `https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/GetAVC`
  - `https://www.sopor.nu/umbraco/surface/AvfallshubbenSurface/GetAvc/`
- **Authentication**: None
- **Query Parameters**:
  - `externalAvcId` *(required, string)*: The center identifier (e.g. `246301`)
  - `municipalityCode` *(required, string)*: The 4-digit municipality code (e.g. `2463`)

#### Example Request
```bash
curl -G "https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/GetAVC" \
  --data-urlencode "externalAvcId=246301" \
  --data-urlencode "municipalityCode=2463"
```

---

## Field Reference

| Field | Type | Description |
|---|---|---|
| `id` | `string (UUID)` | Internal unique identifier for the ÅVC in Avfallshubben |
| `accountId` | `string (UUID)` | Municipal organisation account managing the center |
| `externalAvcId` | `string` | Publicly displayed recycling center ID |
| `name` | `string` | Facility name (e.g. `"Åsele Återvinningscentral"`) |
| `streetAddress` | `string` | Physical street address |
| `zipCode` | `string` | Postal code |
| `city` | `string` | Postal city name |
| `municipalityCode` | `string` | 4-digit municipality code |
| `lat`, `long` | `string (float)` | WGS84 geographic coordinates |
| `openingHours` | `string` | Free-text opening hours schedule (with line breaks) |
| `openingHoursUrl` | `string` | Direct link to online schedule, calendar, or image |
| `noOfFreeEntries` | `integer / null` | Annual quota of free visits allocated to households |
| `entrySystem` | `string / null` | Barrier/access mechanism (e.g. driving license barcode, app) |
| `proffessionalInfo` | `string / null` | Terms, billing, and entry rules for commercial businesses |
| `contactEmail` | `string` | Customer support email address |
| `contactPhone` | `string` | Customer support telephone number |
| `url` | `string` | Official municipal waste website |
| `fractionIds` | `string (comma-separated)` | IDs of all accepted waste fractions at this facility |

---

### 3. HTML Accordion Endpoint (`AvcSurface/GetAvc`)

When a user clicks on an ÅVC on `sopor.nu`, the web application loads a pre-rendered HTML accordion containing icons and descriptions of all accepted waste fractions:

- **Method**: `GET`
- **URL**: `https://www.sopor.nu/umbraco/surface/AvcSurface/GetAvc/`
- **Query Parameters**: `externalAvcId`, `municipalityCode`

#### Accepted Fraction Categories (from the HTML view)
Each fraction is rendered with an SVG icon and official Swedish label:

| Category Name (Swedish) | English Translation | Typical SVG Icon Path |
|---|---|---|
| **Farligt Avfall** | Hazardous waste (chemicals, paint, oils) | `/media/hfnpisiu/farligt.svg` |
| **Elavfall** | Electronic waste (appliances, IT equipment) | `/media/ktylevay/elavfall.svg` |
| **Grovplast** | Bulky plastic items (furniture, toys, buckets) | `/media/g50jat2z/hardplast.svg` |
| **Metall** | Scrap metal & metal packaging | `/media/yyoppvkc/metallskrot.svg` |
| **Trädgårdsavfall** | Garden waste (branches, leaves, lawn clippings) | `/media/u5njzr1z/tradgardsavfall.svg` |
| **Byggavfall** | Demolition & construction debris (concrete, tiles) | `/media/3lrcpshg/betong.svg` |
| **Energiåtervinning** | Combustible waste for district heating | `/media/mp5hfrpu/energiatervinning.svg` |
| **Ej återvinningsbart** | Non-recyclable landfill waste | `/media/wo4ae31r/ejatervinningsbart.svg` |
| **Textilavfall** | Textiles & clothes (reusable or damaged) | `/media/fgdbbjny/trasig_textil_rgb.svg` |
| **Pappersförpackningar** | Paper & cardboard packaging | `/media/a3inob1g/forpackningar.svg` |
| **Plastförpackningar** | Household plastic packaging | `/media/1exezpuy/plast.svg` |
| **Metallförpackningar** | Household metal tins & cans | `/media/fkvja4vu/metall.svg` |
| **Tidningar & trycksaker**| Newspapers, catalogs & flyers | `/media/at3pyjl2/tidningar.svg` |
| **Batterier** | Household batteries & car batteries | `/media/fh4pt0jn/batterier.svg` |
| **Färgade glasförpackningar** | Coloured glass bottles & jars | `/media/wwlflliw/fargat-glas.svg` |
| **Ofärgade glasförpackningar** | Clear glass bottles & jars | `/media/stwdqs0q/ofargat-glas.svg` |
