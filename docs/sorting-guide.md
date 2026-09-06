# National Waste Sorting Guide (Sorteringsguide) API

The **Sorteringsguide** on `sopor.nu` provides authoritative instructions on how everyday consumer items, packaging, and household waste products must be sorted in Sweden according to national environmental standards.

---

## Endpoints

### 1. Autocomplete / Item Taxonomy (`AutocompleteApi/GetStrings`)

Retrieves the complete list of 1,199 standardized item names and materials indexed in the sorting guide.

- **Method**: `GET`
- **URL**: `https://www.sopor.nu/umbraco/api/AutocompleteApi/GetStrings`
- **Authentication**: None
- **Query Parameter**:
  - `culture` *(string, default: `sv-se`)*: Language locale

#### Example Request

```bash
curl "https://www.sopor.nu/umbraco/api/AutocompleteApi/GetStrings?culture=sv-se"
```

#### Example Response (`200 OK`)

Returns a JSON array of 1,199 item strings:

```json
[
  "Grenar",
  "Löv",
  "Blast",
  "Plastflaska",
  "Ketchupflaska - plast",
  "Tandkrämstub",
  "Gräs",
  "Matrester",
  "Tandborste",
  "Tandborste - elektrisk",
  "Stekpanna",
  "Kaffekapsel",
  "Nagellack",
  "Målarfärg",
  "Bord"
]
```

---

### 2. Item Fraction Resolution

Queries the sorting guide to retrieve the destination waste stream, disposal guidance, and icon for a specific item.

- **Method**: `GET`
- **URL**: `https://www.sopor.nu/sortera-och-aatervinn/sorteringsguide/`
- **Authentication**: None
- **Query Parameters**:
  - `searchTerm` *(required, string)*: The item name (e.g. `Tandborste` or `Ketchupflaska`)
  - `lang` *(string)*: `sv-se`
  - `pageSize` *(integer)*: Number of results per page (default: `10`)
  - `page` *(integer)*: Page index (0-indexed)

#### Example Request

```bash
curl -G "https://www.sopor.nu/sortera-och-aatervinn/sorteringsguide/" \
  --data-urlencode "searchTerm=Tandborste" \
  --data-urlencode "lang=sv-se"
```

#### Result HTML Structure

The response returns HTML containing `<div class="recycleSearchResult">` blocks:

```html
<div class="recycleSearchResult">
  <div class="d-flex align-items-center recycleSearchResult-header">
    <img src="/media/fwrc24qq/restavfall.svg" alt="Restavfall" class="img-fluid me-3" />
    <div>
      <h2 class="m-0">Tandborste</h2>
      <p class="mb-0">Vanliga tandborstar sorteras som restavfall (hushållssopor).</p>
    </div>
  </div>
</div>

<div class="recycleSearchResult">
  <div class="d-flex align-items-center recycleSearchResult-header">
    <img src="/media/azdi3ghq/elavfall.svg" alt="Elavfall" class="img-fluid me-3" />
    <div>
      <h2 class="m-0">Tandborste - elektrisk</h2>
      <p class="mb-0">Eltandborstar innehåller elektronik och batterier och ska lämnas som elavfall på återvinningscentralen eller i butik.</p>
    </div>
  </div>
</div>
```

---

## Standard Target Fractions

The sorting guide maps all 1,199 items into one of the following official disposal destinations:

| Fraction Name | Primary Disposal Location | Example Items |
| --- | --- | --- |
| **Matavfall** | Brown household food waste bin | Matrester, blast, kaffesump |
| **Restavfall** | Grey/black household garbage bin | Tandborste, disktrasa, kuvert, dammsugarpåse |
| **Pappersförpackningar** | ÅVS (Green station) or property bin | Mjölkkartong, flingpaket, wellpappkartong |
| **Plastförpackningar** | ÅVS (Green station) or property bin | Schampoflaska, plastfolie, chipspåse |
| **Metallförpackningar** | ÅVS (Green station) or property bin | Konservburk, metallock, värmeljuskopp |
| **Färgade glasförpackningar** | ÅVS (Green station) or property bin | Vinflaska, ölflaska |
| **Ofärgade glasförpackningar** | ÅVS (Green station) or property bin | Syltburk, barnmatsburk |
| **Tidningar & trycksaker** | ÅVS (Green station) or property bin | Dagstidning, magasin, reklam |
| **Farligt avfall** | ÅVC (Recycling center) or mobile miljöbil | Nagellack, målarfärg, lösningsmedel, sprayburk |
| **Elavfall** | ÅVC (Recycling center) or electronics store | Brödrost, hörlurar, eltandborste, sladdar |
| **Batterier** | Batteriholk (battery box) or ÅVC | AA/AAA-batterier, knappcellsbatterier |
| **Grovavfall** | ÅVC (Recycling center) | Möbler, cyklar, mattor, madrasser |
| **Trädgårdsavfall** | ÅVC (Recycling center) | Grenar, löv, gräsklipp |
| **Apotek** | Local pharmacy | Överblivna läkemedel, sprutor |

---

## Python Extraction Example

To extract and compile the entire Swedish sorting guide into a local JSON or CSV file:

```python
import requests
import re
from bs4 import BeautifulSoup

# 1. Fetch complete item taxonomy
items_url = "https://www.sopor.nu/umbraco/api/AutocompleteApi/GetStrings?culture=sv-se"
items = requests.get(items_url).json()

print(f"Discovered {len(items)} items in the national guide.")

# 2. Resolve an item's disposal instructions
def resolve_item(term):
    url = "https://www.sopor.nu/sortera-och-aatervinn/sorteringsguide/"
    resp = requests.get(url, params={"searchTerm": term, "lang": "sv-se"})
    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    for card in soup.select(".recycleSearchResult"):
        name = card.select_one("h2")
        desc = card.select_one("p")
        img = card.select_one("img")

        results.append({
            "name": name.text.strip() if name else "",
            "fraction": img.get("alt", "") if img else "",
            "instructions": desc.text.strip() if desc else "",
            "iconUrl": img.get("src", "") if img else "",
        })
    return results

print("Sample resolution for 'Tandkrämstub':", resolve_item("Tandkrämstub"))
```
