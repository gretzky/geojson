# geojson

GeoJSON datasets of:

- Continents
- Regions & Subregions (as defined by the [UN Geoscheme](https://en.wikipedia.org/wiki/United_Nations_geoscheme))
- Countries and their [administrative divisions](https://en.wikipedia.org/wiki/Administrative_division)
- Major Bodies of Water
- Timezones (as defined by the [tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))

## Usage

The current version of the data is **4.1**. If GADM has updated and the administrative data for countries needs to be rescraped, do the following:

- Ensure you have python and pip 3 installed
- Install packages: `pip3 install -r requirements.txt`
- Run the scraper: `python3 ./scripts/countries.py`

The scraper does the following:

- Clears old GADM data from `geojson/countries`
- Gets all ISO 3166-1 alpha3 country codes (250) with available datasets on GADM
- Scrapes GADM by country code and populates a directory for each country with all [administrative division](https://en.wikipedia.org/wiki/Administrative_division) data available
  - `admin_0` describes the boundaries of the country itself
  - First order administrative level data (ISO 3166-2) (`admin_1`) is available for all but 49 countries
  - Administrative divisions up to fourth-level are available where applicable
