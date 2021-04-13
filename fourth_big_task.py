import os
import sys
import pygame
import requests

spn = ['0.005 0.005', '0.01 0.01', '0.05 0.05', '0.1 0.1', '0.25 0.25', '0.5 0.5', '1 1', '2 2',
       '5 5', '10 10', '20 20', '30 30', '50 50']
k = 1


def buttons():
    for i in range(3):
        if Buttons[i]:
            screen.blit(second_button, (575, 300 + 25 * i))
        else:
            screen.blit(first_button, (575, 300 + 25 * i))


def load_map(coords='39 52', spn='0.005 0.005', l='map'):
    api_server = "http://static-maps.yandex.ru/1.x/"

    params = {
        'll': ','.join(coords.split()),
        'spn': ','.join(spn.split()),
        "l": l
    }
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(response)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return response.content


map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(load_map())

Buttons = [False, False, False]
first_button = pygame.transform.scale(pygame.image.load('data/кнопка1.png'), (25, 25))
second_button = pygame.transform.scale(pygame.image.load('data/кнопка2.png'), (25, 25))

pygame.init()
screen = pygame.display.set_mode((600, 450))
pygame.display.flip()
running = True
clock = pygame.time.Clock()
img = pygame.image.load(map_file)
l_need = ['map', 'sat', 'sat,skl']
first_c, sec_c = 39, 52
FPS = 40
while running:
    try:
        with open(map_file, "wb") as file:
            try:
                file.write(load_map(spn=spn[k], l=l_need[Buttons.index(True)],
                                    coords=' '.join([str(i) for i in [first_c, sec_c]])))
            except ValueError:
                file.write(load_map(spn=spn[k],
                                    coords=' '.join([str(i) for i in [first_c, sec_c]])))
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    screen.blit(pygame.image.load(map_file), (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == 281:
                if k < len(spn) - 1:
                    k += 1
            elif event.key == 280:
                if k > 0:
                    k -= 1
            elif event.key == pygame.K_UP:
                sec_c += (float(spn[k].split()[0]) * 2)
            elif event.key == pygame.K_DOWN:
                sec_c -= (float(spn[k].split()[0]) * 2)
            elif event.key == pygame.K_RIGHT:
                first_c += (float(spn[k].split()[1]) * 2)
            elif event.key == pygame.K_LEFT:
                first_c -= (float(spn[k].split()[1]) * 2)
            if first_c >= 180:
                first_c -= 359
            elif first_c <= - 180:
                first_c += 359
            if sec_c >= 86:
                sec_c -= 171
            elif sec_c <= -86:
                sec_c += 171
        if event.type == pygame.MOUSEBUTTONDOWN:
            if second_button.get_rect(x=575, y=300).collidepoint(event.pos):
                Buttons = [True, False, False]
            elif second_button.get_rect(x=575, y=325).collidepoint(event.pos):
                Buttons = [False, True, False]
            elif second_button.get_rect(x=575, y=350).collidepoint(event.pos):
                Buttons = [False, False, True]

    buttons()
    pygame.display.flip()
    clock.tick(FPS)

os.remove(map_file)
pygame.quit()
