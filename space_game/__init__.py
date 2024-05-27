import pygame
import sys
from .game_object import GameObject
from .helpers import handle_json


def quit(run) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit(0)


def create_game(screen) -> None:
    objects = {}

    player = GameObject.game_from_json("game_data.json")
    player.draw(screen)

    objects.update({"player": player})

    return objects


# create_game()
