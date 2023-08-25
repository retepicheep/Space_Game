import pygame
from consts import *
from random import randint
from objcets import *


class Background:
    def __init__(self, color) -> None:
        self.color = color
        self.objects = []

    def generate(self, surface, place):
        if place == "space":
            rect = (0, 0, WIDTH, HEIGHT)
            pygame.draw.rect(surface, self.color, rect)
            num = 0
            while num < 11:
                obj = Planet(randint(1, HEIGHT), randint(1, WIDTH), surface, num)
                obj.build()
                self.objects.append(obj)
                num += 1

    def build(self, obj):
        obj.build()
