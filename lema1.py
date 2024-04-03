import json
import requests

url = "https://lamadeleine.com/wp-json/wp/v2/restaurant-locations?per_page=150"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)

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

# Use the function to parse the JSON data
location_info = extract_location_info(data)

# Print the extracted information
for info in location_info:
    print(json.dumps(info, indent=2))