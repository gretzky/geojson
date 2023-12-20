import requests
from bs4 import BeautifulSoup
import json
from zipfile import ZipFile
from io import BytesIO
import os

# clean out all old gadm data
def clear_country_data():
    for subdir, dirs, files in os.walk(f"geojson/countries"):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file != 'properties.json':
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

# get a list of all ISO 3166 alpha-3 country codes from GADM
def scrape_country_codes():
    url = 'https://gadm.org/download_country.html'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    select_element = soup.find('select', {'id': 'countrySelect'})
    country_codes = {}
    if select_element:
        options = select_element.find_all('option')
        for option in options:
            value = option['value']
            if value:
                code = value.split('_')[0]
                country_name = option.text
                country_codes[code] = country_name
    return country_codes

# scrape administrative data for each country
def scrape_country_admin_data(country_code, level, gadm_version='4.1'):
    clear_country_data()
    
    if not isinstance(gadm_version, str):
        gadm_version = str(gadm_version)

    flat_version = gadm_version.replace('.','')

    gadm_url = f'https://geodata.ucdavis.edu/gadm/gadm{gadm_version}/json/gadm{flat_version}_'

    # Create a directory for the country if it doesn't exist
    country_dir = os.path.join('geojson', 'countries', f"{country_code}")
    os.makedirs(country_dir, exist_ok=True)

    # URL for the main JSON file
    main_url = gadm_url + f"{country_code}_0.json"
    
    # Download the main JSON file
    response = requests.get(main_url)
    data = response.json()
    with open(f"{country_dir}/admin_0.geojson", 'w') as geojson_file:
        json.dump(data, geojson_file)

    # Check for additional URLs
    for additional_level in range(1, level):
        additional_url = gadm_url + f"{country_code}_{additional_level}.json.zip"
        
        # Download the additional JSON.zip file
        response = requests.get(additional_url)
        
        if response.status_code == 200:
            # Convert the response content to BytesIO
            zip_content = BytesIO(response.content)

            # Extract the content of the ZIP file
            with ZipFile(zip_content) as zip_file:
                # Find the JSON file in the ZIP archive
                json_file_name = None
                for file_name in zip_file.namelist():
                    if file_name.endswith('.json'):
                        json_file_name = file_name
                        break

                if json_file_name:
                    # Read the JSON file from the ZIP and parse it
                    with zip_file.open(json_file_name) as json_file:
                        try:
                            additional_data = json.load(json_file)
                        except json.JSONDecodeError:
                            # If JSON decoding fails, assume it's HTML content and use BeautifulSoup
                            html_content = json_file.read()
                            soup = BeautifulSoup(html_content, 'html.parser')
                            additional_data = soup.prettify()

                    # Save the additional data to a file
                    with open(f"{country_dir}/admin_{additional_level}.geojson", 'w') as geojson_file:
                        json.dump(additional_data, geojson_file)



country_codes = scrape_country_codes()
for country_code in country_codes:
    scrape_country_admin_data(country_code, 5)
