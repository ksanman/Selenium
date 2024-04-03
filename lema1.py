import requests

url = "https://lamadeleine.com/wp-json/wp/v2/restaurant-locations?per_page=150"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Failed to retrieve data, status code:", response.status_code)
