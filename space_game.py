import pygame
from main_functions import *

pygame.init()

init_dict = handle_json(("init.json", "r", None))[0]

win_x, win_y = init_dict["win_x"], init_dict["win_y"]
screen = pygame.display.set_mode((win_x, win_y))

clock = pygame.time.Clock()

run = True
create_game(screen)
while run:
    quit(run)

    clock.tick(60)

    pygame.display.update()
