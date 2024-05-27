import pygame
import sys
from .game_object import GameObject
from .helpers import handle_json
from random import randint


def quit(run) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit(0)


def resize(objects):
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            win_x, win_y = event.size

            # Calculate offset between player's position and screen center
            player_offset_x = win_x // 2 - objects["player"].pos_x
            player_offset_y = win_y // 2 - objects["player"].pos_y

            # Update positions of other objects relative to the player's position and the screen center
            for obj in objects:
                if obj != objects["player"]:  # Exclude player object
                    objects[obj].update(x=player_offset_x, y=player_offset_y)


def create_game(screen) -> None:
    objects = {}

    player = GameObject.game_from_json("game_data.json", ["player"])
    player.draw(screen)

    objects.update({"player": player})

    planets = set()
    if handle_json("game_data.py", "read", keywords=["planets"]) is not None:
        for obj in range(
            len(handle_json("game_data.py", "read", keywords=["planets"]))
        ):
            planet = GameObject.game_from_json("game_data.json", ["planets", str(obj)])
            planets.add(planet)
    else:
        for obj2 in range(randint(5, 10)):
            size = randint(64, 100)
            planet = GameObject(
                randint(-800, 800),
                randint(-800, 800),
                (size, size),
                randint(0, 360),
                "planet",
                f"planet#{obj2}",
                f"assets/planets/planet{randint(0, 10)}.png",
            )
            collision = False
            for pl in planets:
                if planet.check_collision(pl):
                    collision = True
                    obj2 -= 1
                    break

            if not collision:
                planets.add(planet)

    return objects


# create_game()
