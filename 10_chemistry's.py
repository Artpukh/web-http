import sys
import requests
from get_lines import get_coordinates
import pygame
import os

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
address = get_coordinates(' '.join(sys.argv[1:]))
address = ','.join(list(map(lambda x: str(x), address)))


search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
json_response = response.json()
organizations = json_response["features"][:11]
spis = []
delta = "0.05"
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address,
    "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
}
for k, i in enumerate(organizations):
    name = i["properties"]["CompanyMetaData"]["name"]
    adr = i["properties"]["CompanyMetaData"]["address"]
    point = i["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    hours = i["properties"]["CompanyMetaData"]["Hours"]
    if "TwentyFourHours" in hours["Availabilities"][0]:
        if 'pt' not in map_params:
            map_params['pt'] = f'{org_point},pm2dgm'
        else:
            map_params['pt'] += f'~{org_point},pm2dgm'
    elif "Intervals" in hours["Availabilities"][0]:
        if 'pt' not in map_params:
            map_params['pt'] = f'{org_point},pm2rdm'
        else:
            map_params['pt'] += f'~{org_point},pm2rdm'
    else:
        if 'pt' not in map_params:
            map_params['pt'] = f'{org_point},pm2grm'
        else:
            map_params['pt'] += f'~{org_point},pm2grm'


map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
print(response.url)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)


pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
# Москва, ул. Ак. Королева, 12