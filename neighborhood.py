from get_lines import get_coordinates, geocode
import sys
import requests
api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

address = get_coordinates(' '.join(sys.argv[1:]))
address = ','.join(list(map(lambda x: str(x), address)))

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

params = {
    "apikey": api_key,
    "geocode": address,
    "kind": "district",
    "format": "json",
}
response = requests.get(geocoder_api_server, params=params)
json_response = response.json()
print(json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]
      ["GeocoderMetaData"]["Address"]["Components"][5]["name"])

# Москва, ул. Ак. Королева, 12