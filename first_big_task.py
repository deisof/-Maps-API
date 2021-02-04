import os
import sys

import pygame
import requests

SPN1 = "0.002"
SPN2 = "0.002"
COORD1 = "39.573160"
COORD2 = "52.619412"

api_server = "http://static-maps.yandex.ru/1.x/"

params = {
    "ll": ",".join([COORD1, COORD2]),
    "spn": ",".join([SPN1, SPN2]),
    "l": "map"
}
response = requests.get(api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(response)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
