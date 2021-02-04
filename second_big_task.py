import os
import sys

import pygame
import requests

SPN1 = "0.002"
SPN2 = "0.002"
COORD1 = "39.573160"
COORD2 = "52.619412"

spn = ["0.002 0.002", "0.016457 0.00619", "0.3 0.3", "0.5 0.5", "10 10"]
k = 1


def load_map():
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

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

    os.remove(map_file)


pygame.init()
screen = pygame.display.set_mode((600, 450))
load_map()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if k != (len(spn) - 1):
                    SPN1, SPN2 = spn[k].split(' ')
                    k += 1
                    load_map()
                else:
                    SPN1, SPN2 = spn[-1].split(' ')
                    load_map()
            if event.key == pygame.K_PAGEDOWN:
                if k >= 0:
                    SPN1, SPN2 = spn[k].split(' ')
                    k -= 1
                    load_map()
                else:
                    SPN1, SPN2 = spn[0].split(' ')
                    load_map()

pygame.quit()
