import pygame
import sys
from pytmx import pytmx
from settings import *
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)
tmx_data = load_pygame('Tiled/data/Maze.tmx')
clock = pygame.time.Clock()

# assign a rectangle to tiles that are collidable
def get_collidable_tiles(tmx_data):
    collidable_tiles = []
    layer = tmx_data.get_layer_by_name('walls')
    for x, y, gid in layer:
        tile = tmx_data.get_tile_image_by_gid(gid)
        if tile:
            collidable_tiles.append(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight, tmx_data.tilewidth, tmx_data.tileheight))
    return collidable_tiles

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.walk_right_sprites = []
        self.walk_left_sprites = []
        self.walk_up_sprites = []
        self.walk_down_sprites = []
        self.load_sprites()

        self.current_sprite = 0
        self.image = self.walk_right_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        self.is_moving = False

    def load_sprites(self):
        for j in range(4):
            img = pygame.image.load(
                f'Minifantasy_CreaturesHumanBaseWalk/Minifantasy_CreaturesHumanBaseWalk_{j}.png').convert_alpha()
            img = pygame.transform.rotozoom(img, 0, 3)
            self.walk_right_sprites.append(img)
        for j in range(4, 8):
            img = pygame.image.load(
                f'Minifantasy_CreaturesHumanBaseWalk/Minifantasy_CreaturesHumanBaseWalk_{j}.png').convert_alpha()
            img = pygame.transform.rotozoom(img, 0, 3)
            self.walk_left_sprites.append(img)
        for j in range(8, 12):
            img = pygame.image.load(
                f'Minifantasy_CreaturesHumanBaseWalk/Minifantasy_CreaturesHumanBaseWalk_{j}.png').convert_alpha()
            img = pygame.transform.rotozoom(img, 0, 3)
            self.walk_up_sprites.append(img)
        img = pygame.image.load(
            f'Minifantasy_CreaturesHumanBaseWalk/Minifantasy_CreaturesHumanBaseWalk_{1}.png').convert_alpha()
        img = pygame.transform.rotozoom(img, 0, 3)
        self.walk_down_sprites.append(img)
        img = pygame.image.load(
            f'Minifantasy_CreaturesHumanBaseWalk/Minifantasy_CreaturesHumanBaseWalk_{3}.png').convert_alpha()
        img = pygame.transform.rotozoom(img, 0, 3)
        self.walk_down_sprites.append(img)
        img = pygame.image.load(
            f'Minifantasy_CreaturesHumanBaseWalk/Minifantasy_CreaturesHumanBaseWalk_{5}.png').convert_alpha()
        img = pygame.transform.rotozoom(img, 0, 3)
        self.walk_down_sprites.append(img)

        img = pygame.image.load(
            f'Minifantasy_CreaturesHumanBaseWalk/Minifantasy_CreaturesHumanBaseWalk_{7}.png').convert_alpha()
        img = pygame.transform.rotozoom(img, 0, 3)
        self.walk_down_sprites.append(img)

    def animate_right(self):
        if self.is_moving:
            self.current_sprite += ANIMATION_SPEED
            self.image = self.walk_right_sprites[int(self.current_sprite) % len(self.walk_right_sprites)]

    def animate_left(self):
        if self.is_moving:
            self.current_sprite += ANIMATION_SPEED
            self.image = self.walk_left_sprites[int(self.current_sprite) % len(self.walk_left_sprites)]

    def animate_up(self):
        if self.is_moving:
            self.current_sprite += ANIMATION_SPEED
            self.image = self.walk_up_sprites[int(self.current_sprite) % len(self.walk_up_sprites)]

    def animate_down(self):
        if self.is_moving:
            self.current_sprite += ANIMATION_SPEED
            self.image = self.walk_down_sprites[int(self.current_sprite) % len(self.walk_down_sprites)]

    def move(self):
        keys = pygame.key.get_pressed()
        if keys:
            self.is_moving = True
            if keys[pygame.K_LEFT]:
                self.animate_left()
                if collision:
                    self.rect.x += 2 * PLAYER_SPEED
                else:
                    self.rect.x -= PLAYER_SPEED
            elif keys[pygame.K_RIGHT]:
                self.animate_right()
                if collision:
                    self.rect.x -= 2 * PLAYER_SPEED
                else:
                    self.rect.x += PLAYER_SPEED
            elif keys[pygame.K_UP]:
                self.animate_up()
                if collision:
                    self.rect.y += 2 * PLAYER_SPEED
                else:
                    self.rect.y -= PLAYER_SPEED
            elif keys[pygame.K_DOWN]:
                self.animate_down()
                if collision:
                    self.rect.y -= 2 * PLAYER_SPEED
                else:
                    self.rect.y += PLAYER_SPEED
        self.is_moving = False

    def update(self):
        self.move()


def display_level(tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

def check_collision(sprite, walls):
    for wall in walls:
        if sprite.rect.colliderect(wall):
            return True

player = pygame.sprite.GroupSingle()
player.add(Player(300, 300))

collidable_tiles = get_collidable_tiles(tmx_data)
collision = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    display_level(tmx_data)
    collision = check_collision(player.sprite, collidable_tiles)
    player.draw(screen)
    player.update()
    pygame.display.update()
    clock.tick(60)

# TODO: fix player movement upper collision
