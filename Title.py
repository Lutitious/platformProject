import pygame
from pygame.locals import *

pygame.init()
SIZE = (600, 400)
screen = pygame.display.set_mode(SIZE)
# --- surface to stretch the screen
TitleScreen = pygame.image.load("TitleScreen.png")
# Surface to be stretched:
w = int(TitleScreen.get_width())
h = int(TitleScreen.get_height())
display = pygame.Surface((w, h))
loop = 1
while loop:
    display.fill((0, 0, 128))
    display.blit(TitleScreen, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            loop = 0
    screen.blit(pygame.transform.scale(display, SIZE), (0, 0))
    pygame.display.update()

pygame.quit()