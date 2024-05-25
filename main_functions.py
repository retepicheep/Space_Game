import pygame
import json
import sys

import os
from objects import *


def handle_json(*json_files) -> list:
    """This function takes a tupel contraining,
    a json file path, a open method, and a keyword to return.
    It then proforms the operation loading the items into a
    list to be returned to you."""

    return_dicts = []

    try:
        for json_file in json_files:
            file = json_file[0]
            method = json_file[1]
            keyword = json_file[2]
            with open(file, method) as f:
                if keyword == str:
                    return_dict = json.loads(f.read())[keyword]
                else:
                    return_dict = json.loads(f.read())
                return_dicts.append(return_dict)
    except FileNotFoundError:
        print(
            "The file 'data.json' was not found. Please make sure it is in the correct directory."
        )
    except json.JSONDecodeError:
        print("The file 'data.json' is not a valid JSON file.")
    except KeyError:
        print("The key 'init' was not found in the JSON file.")

    return return_dicts


def quit(run) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit(0)


def create_game(screen) -> None:
    player_data = handle_json(("game_data.json", "r", "player"))[0]["player"]

    # print(os.path.abspath(player_data["sprite"]))

    player = GameObject(
        player_data["pos_x"],
        player_data["pos_y"],
        eval(player_data["size"]),
        player_data["object_type"],
        player_data["name"],
        player_data["sprite"],
    )
    player.update(screen)


# create_game()
