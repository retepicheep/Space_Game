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


def repos(objects):
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            win_x, win_y = event.size
            print(win_x, win_y)

            # Calculate offset between player's current position and the new center of the screen
            player = objects["player"]
            center_x = win_x // 2
            center_y = win_y // 2

            offset_x = center_x - player.pos_x
            offset_y = center_y - player.pos_y

            # Update player's position to the center of the screen
            player.pos_x = center_x
            player.pos_y = center_y
            player.update()

            # Update positions of other objects relative to the player's new position
            for obj_key, obj in objects.items():
                if obj_key != "player":  # Exclude player object
                    obj.update(x=offset_x, y=offset_y)


def create_game(screen) -> None:
    objects = {}

    player = GameObject.game_from_json("game_data.json", ["player"])
    player.draw(screen)

    objects.update({"player": player})

    places = set()
    if handle_json("game_data.py", "read", keywords=["places"]) is not None:
        for obj in range(len(handle_json("game_data.py", "read", keywords=["places"]))):
            place = GameObject.game_from_json("game_data.json", ["places", str(obj)])
            places.add(place)
    else:
        for obj2 in range(randint(5, 10)):
            size = randint(400, 600)
            place = GameObject(
                randint(-800, 800),
                randint(0, 100),
                (size, size),
                randint(0, 360),
                "place",
                f"place#{obj2}",
                f"assets/places/planet{randint(0, 10)}.png",
                ["places", f"place#{obj2}"],
            )
            collision = False
            for pl in places:
                if place.check_collision(pl):
                    collision = True
                    obj2 -= 1
                    break

            if not collision:
                places.add(place)
                place.update()
                place.draw(screen)
                objects.update({f"place#{obj2}": place})

    return objects


# create_game()


def draw_minimap(
    screen,
    objects,
    player,
    win_x,
    win_y,
    minimap_width,
    minimap_height,
    minimap_scale,
):
    minimap_surface = pygame.Surface((minimap_width, minimap_height))
    minimap_surface.fill((0, 0, 0, 255))
    for obj in objects.values():
        obj.draw_on_minimap(minimap_surface, minimap_scale)
    screen.blit(minimap_surface, (win_x - minimap_width, win_y - minimap_height))
