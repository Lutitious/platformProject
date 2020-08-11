import pygame
import math
import itertools
from pygame.locals import *


def magnitude(v):
    return math.sqrt(sum(v[j] * v[j] for j in range(len(v))))


def sub(u, v):
    return [u[j] - v[j] for j in range(len(u))]


def normalize(v):
    return [v[j] / magnitude(v) for j in range(len(v))]


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Game')
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
buttons = ['up', 'down', 'left', 'right', 'start', 'A', 'B', 'X', 'Y', 'L', 'R']
WINDOW_SIZE = (600, 400)
display = pygame.Surface((300, 200))
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
moving_right = False
moving_left = False
stay_right = True
sprinting = False
momentum = 0
air_timer = 0
path = itertools.cycle([(26, 43), (105, 110), (45, 225), (145, 295), (266, 211), (178, 134), (250, 56), (147, 12)])
target = next(path)
ball, speed = pygame.rect.Rect(target[0], target[1], 10, 10), 3.6
pause_text = pygame.font.SysFont('Ubuntu', 32).render('Pause', True, pygame.color.Color('White'))

game_map1 = """
x----xxxxxx----xxxx
oxx----ooo-------oo
o------ooo--------o
o---xxxoo-----xxxxo
o------ooxxxx-----o
oxxx---oo-------xxo
o------oo---------o
o---xxxooxxxxxxxx-o
o------oo---------o
oxxxxxxoo-xxxxxxxxo
ooooooooo----------
ooooooooooooooooooo
""".splitlines()

game_map = [list(lst) for lst in game_map1]

tl = {}
tl["o"] = dirt_img = pygame.image.load('dirt.jpg')
tl["x"] = grass_img = pygame.image.load('grass.jpg')

player_img = pygame.image.load('player.png').convert()
player_img.set_colorkey((255, 255, 255))
player_rect = pygame.Rect(100, 100, 5, 13)


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {
        'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


loop = 1
while loop:
    display.fill((146, 244, 255))
    tile_rects = []
    y = 0
    for line_of_symbols in game_map:
        x = 0
        for symbol in line_of_symbols:
            if symbol in tl:
                display.blit(
                    tl[symbol], (x * 16, y * 16))
            if symbol != "-":
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1
    player_movement = [0, 0]
    if moving_right:
        if sprinting:
            player_movement[0] += 2
        else:
            player_movement[0] += 1
    if moving_left:
        if sprinting:
            player_movement[0] -= 2
        else:
            player_movement[0] -= 1
    player_movement[1] += momentum
    momentum += 0.3
    if momentum > 3:
        momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        air_timer = 0
        momentum = 0
    else:
        air_timer += 1
    if stay_right:
        display.blit(
            player_img, (player_rect.x, player_rect.y))
    else:
        display.blit(
            pygame.transform.flip(player_img, True, False),
            (player_rect.x, player_rect.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            loop = 0
        if event.type == KEYDOWN:
            if event.key in [K_RIGHT, K_d]:
                moving_right = True
                stay_right = True
            if event.key in [K_LEFT, K_a]:
                moving_left = True
                stay_right = False
            if event.key in [K_LSHIFT]:
                sprinting = True
            if event.key in [K_SPACE]:
                if air_timer < 6:
                    momentum = -5
        if event.type == KEYUP:
            if event.key in [K_RIGHT, K_d]:
                moving_right = False
            if event.key in [K_LEFT, K_a]:
                moving_left = False
            if event.key in [K_LSHIFT]:
                sprinting = False
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            joy_name = joystick.get_name()
            if "xbox" in joy_name.lower():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button in [0, 1]:
                        if air_timer < 6:
                            momentum = -5
                    if event.button in [2, 3]:
                        sprinting = True
                if event.type == pygame.JOYBUTTONUP:
                    if event.button in [2, 3]:
                        sprinting = False
                if event.type == pygame.JOYHATMOTION:
                    if event.value[0] == 1:
                        moving_right = True
                    if event.value[0] == -1:
                        moving_left = True
                    if event.value[0] == 0:
                        moving_right = False
                        moving_left = False
                x_axis = joystick.get_axis(0)
                if x_axis > 0.5:
                    moving_right = True
                if x_axis < -0.5:
                    moving_left = True
                if -0.5 < x_axis < 0.5:
                    moving_left = False
                    moving_right = False
            if "joy-con" in joy_name.lower():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button in [1, 0]:
                        if air_timer < 6:
                            momentum = -5
                    if event.button in [2, 3]:
                        sprinting = True
                if event.type == pygame.JOYBUTTONUP:
                    if event.button in [2, 3]:
                        sprinting = False
                if event.type == pygame.JOYHATMOTION:
                    if event.value[0] == 1:
                        moving_right = True
                    if event.value[0] == -1:
                        moving_left = True
                    if event.value[0] == 0:
                        moving_right = False
                        moving_left = False
            if "switch" or "lira" or "pro cont" in joy_name.lower():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button in [1, 2]:
                        if air_timer < 6:
                            momentum = -5
                    if event.button in [0, 3]:
                        sprinting = True
                if event.type == pygame.JOYBUTTONUP:
                    if event.button in [2, 3]:
                        sprinting = False
                if event.type == pygame.JOYHATMOTION:
                    if event.value[0] == 1:
                        moving_right = True
                    if event.value[0] == -1:
                        moving_left = True
                    if event.value[0] == 0:
                        moving_right = False
                        moving_left = False
                x_axis = joystick.get_axis(0)
                if x_axis > 0.35:
                    moving_right = True
                if x_axis < -0.35:
                    moving_left = True
                if -0.35 < x_axis < 0.35:
                    moving_left = False
                    moving_right = False
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
