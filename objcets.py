import pygame
import os
from consts import *
from random import randint


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, surface, route) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.surface = surface
        self.route = route

    def build(self):
        img = pygame.image.load(self.route)
        self.rect = img.get_rect()
        self.surface.blit(img, (self.x, self.y))


class Planet(GameObject):
    def __init__(self, x, y, surface, num, map_num=None):
        self.surface = surface
        self.map_num = map_num
        self.num = num
        self.type = "planet"
        self.img = f"assets/planets/planet{num}.png"
        img = pygame.image.load(self.img).convert_alpha()
        self.mask = pygame.mask.from_surface(img)
        super().__init__(x, y, self.surface, os.path.join(self.img))
