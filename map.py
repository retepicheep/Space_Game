import pygame
from consts import *
from random import randint
from objcets import *


class Background:
    def __init__(self) -> None:
        self.objects = []

    def generate(self, surface, group, group_num, c):
        num = 0
        while num < group_num:
            obj = c(randint(1, HEIGHT), randint(1, WIDTH), surface, num)
            group.add(obj)
            self.objects.append(obj)
            num += 1

    def build(self, obj):
        obj.build()
