import pygame
import sys
from pytmx import pytmx
from settings import *
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)
tmx_data = load_pygame("Tiled/data/basic.tmx")
print(tmx_data.tilewidth, tmx_data.tileheight)


def dispplay_level(tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    dispplay_level(tmx_data)
    pygame.display.update()
