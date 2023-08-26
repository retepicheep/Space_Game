import pygame
import os
from consts import *


class Player(pygame.sprite.Sprite):
    def __init__(self, level) -> None:
        super().__init__()
        self.route = os.path.join(f"assets/players/player{level}.png")
        self.sprite = pygame.image.load(self.route)
        self.img = pygame.transform.scale(self.sprite, (64, 64))
        self.rect = self.img.get_rect()

    def draw(self, surface, dir):
        if dir == "forward":
            self.rect = self.img.get_rect()
            surface.blit(self.img, (400, 400))
        elif dir == "back":
            img = pygame.transform.rotate(self.img, 180)
            self.rect = img.get_rect()
            surface.blit(img, (400, 400))
        elif dir == "right":
            img = pygame.transform.rotate(self.img, 270)
            self.rect = img.get_rect()
            surface.blit(img, (400, 400))
        elif dir == "left":
            img = pygame.transform.rotate(self.img, 90)
            self.rect = img.get_rect()
            surface.blit(img, (400, 400))

    def collided(self, objects):
        objs = pygame.sprite.spritecollide(self, objects, False)
        if objs:
            return objs
        else:
            return False
