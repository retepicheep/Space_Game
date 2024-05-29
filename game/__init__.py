import pygame
import sys
from .game_object import GameObject
from .helpers import handle_json
import math
from pprint import pprint


def quit(run) -> None:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit(0)


def repos(objects, file):
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            win_x, win_y = event.size

            # Calculate offset between player's current position and the new center of the screen
            player = objects["player"]
            center_x = win_x // 2
            center_y = win_y // 2

            offset_x = center_x - player.pos_x
            offset_y = center_y - player.pos_y

            # Update player's position to the center of the screen
            player.pos_x = center_x
            player.pos_y = center_y
            player.update(file)

            # Update positions of other objects relative to the player's new position
            for obj_key, obj in objects.items():
                if obj_key != "player":  # Exclude player object
                    obj.update(file, x=offset_x, y=offset_y)


def create_game(screen, file) -> None:
    objects = {}

    player = GameObject.game_from_json(file, ["player"])
    player.draw(screen)

    objects.update({"player": player})

    # for place in handle_json(file, "read", ["places"]):
    #     pprint(handle_json(file, "read", ["places", place]))

    for pl in range(len(handle_json(file, "read", ["places"]))):
        place = GameObject.game_from_json(file, ["places", f"place{pl}"])
        place.update(file)
        place.draw(screen)
        objects.update({f"{place.name}": place})

    return objects


# create_game()


def draw_pointers(screen, player, objects, win_x, win_y):
    pointer_color = (255, 0, 0)
    pointer_size = 100

    for obj_name, obj in objects.items():
        if obj_name == "player" or obj.is_visible(win_x, win_y):
            continue

        dx = obj.pos_x + player.pos_x
        dy = obj.pos_y + player.pos_y
        angle = math.atan2(dy, dx)

        # Calculate edge intersection
        edge_x, edge_y = None, None
        if abs(math.cos(angle)) > abs(math.sin(angle)):
            edge_x = win_x - 1 if dx > 0 else 0
            edge_y = player.pos_y + (edge_x - player.pos_x) * math.tan(angle)
        else:
            edge_y = win_y - 1 if dy > 0 else 0
            edge_x = player.pos_x + (edge_y - player.pos_y) / math.tan(angle)

        # Clamp to screen edges
        if edge_x < 0:
            edge_x = 0
        if edge_x >= win_x:
            edge_x = win_x - 1
        if edge_y < 0:
            edge_y = 0
        if edge_y >= win_y:
            edge_y = win_y - 1

        # Draw pointer
        pointer_tip = (int(edge_x), int(edge_y))
        pointer_base1 = (
            int(edge_x + pointer_size * math.cos(angle + math.pi / 4)),
            int(edge_y + pointer_size * math.sin(angle + math.pi / 4)),
        )
        pointer_base2 = (
            int(edge_x + pointer_size * math.cos(angle - math.pi / 4)),
            int(edge_y + pointer_size * math.sin(angle - math.pi / 4)),
        )

        pygame.draw.polygon(
            screen, pointer_color, [pointer_tip, pointer_base1, pointer_base2]
        )
