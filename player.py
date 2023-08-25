import pygame
import os
from consts import *


class Player:
    def __init__(self, level) -> None:
        self.route = os.path.join(f"assets/players/player{level}.png")
        self.sprite = pygame.image.load(self.route)
        self.img = pygame.transform.scale(self.sprite, (64, 64))
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, surface, dir):
        if dir == "forward":
            surface.blit(self.img, (400, 400))
            self.mask = pygame.mask.from_surface(self.img)
        elif dir == "back":
            img = pygame.transform.rotate(self.img, 180)
            self.mask = pygame.mask.from_surface(img)
            surface.blit(img, (400, 400))
        elif dir == "right":
            img = pygame.transform.rotate(self.img, 270)
            self.mask = pygame.mask.from_surface(img)
            surface.blit(img, (400, 400))
        elif dir == "left":
            img = pygame.transform.rotate(self.img, 90)
            self.mask = pygame.mask.from_surface(img)
            surface.blit(img, (400, 400))
