import requests
import sys
import os
import pygame
from random import choice as ch
from get_lines import get_ll_span

CITIES = ['Москва', 'Париж', 'Милан', 'Пекин']

city = CITIES.pop(CITIES.index(ch(CITIES)))
ll, span = get_ll_span(city)


api = f'https://static-maps.yandex.ru/1.x/?'
params = {
    "ll": ll,
    "spn": span,
    "l": ch(['map', 'sat'])
}
response = requests.get(api, params=params)
map_file = 'map.png'
with open(map_file, 'wb') as f:
    f.write(response.content)


def change():
    if not CITIES:
        print('Все города отгаданы')
        sys.exit(1)
    city = CITIES.pop(CITIES.index(ch(CITIES)))
    ll, span = get_ll_span(city)
    params = {
        "ll": ll,
        "spn": span,
        "l": ch(['map', 'sat'])
    }
    response = requests.get(api, params=params)
    map_file = 'map.png'
    with open(map_file, 'wb') as f:
        f.write(response.content)



pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            change()
        screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()