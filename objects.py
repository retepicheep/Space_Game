import pygame
# import os


class GameObject:
    def __init__(
        self,
        pos_x,
        pos_y,
        size,
        object_type,
        name,
        sprite,
    ) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.object_type = object_type
        self.name = name
        self.sprite = pygame.transform.scale(pygame.image.load(sprite), self.size)

    def update(self, screen, x=None, y=None):
        if x is None and y is None:
            screen.blit(self.sprite, (self.pos_x, self.pos_y))
        elif x is None and y is not None:
            screen.blit(self.sprite, (self.pos_x, y))
        elif x is not None and y is None:
            screen.blit(self.sprite, (x, self.pos_y))
        else:
            screen.blit(self.sprite, (x, y))
