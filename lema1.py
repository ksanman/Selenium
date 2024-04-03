import json
import requests
import csv

url = "https://lamadeleine.com/wp-json/wp/v2/restaurant-locations?per_page=150"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

def extract_location_info(locations):
    extracted_info = []
    for location in locations:
        info = {
            "locationName": location["acf"]["locationHero"]["storeName"],
            "streetAddress": f'{location["acf"]["locationHero"]["addressLine1"]} {location["acf"]["locationHero"].get("addressLine2", "")}'.strip(),
            "city": location["acf"]["locationHero"]["city"],
            "state": location["acf"]["locationHero"]["state"],
            "postalCode": location["acf"]["locationHero"]["zip"],
            "phoneNumber": location["acf"]["locationHero"]["phone"],
            "storeID": location["id"]
        }
        extracted_info.append(info)
    return extracted_info

#using the function to parse the JSON data
location_info = extract_location_info(data)

#print extracted info
for info in location_info:
    print(json.dumps(info, indent=2))

print(f"Total number of store locations found: {len(location_info)}")

csv_file_name = 'api_store_details.csv'

fieldnames = ['locationName', 'streetAddress', 'city', 'state', 'postalCode', 'phoneNumber', 'storeID']

#writing to the CSV file
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    #writing rows
    for location in location_info:
        writer.writerow(location)

print(f"Data successfully written to {csv_file_name} in the Selenium directory")