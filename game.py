import pygame
from game import handle_json, create_game, quit, repos, draw_pointers
import math

file = "game_data.json"

pygame.init()

init_dict = handle_json("init.json", "read")
# if init_dict is None:
#     print("Failed to read 'init.json'.")
# else:
#     print(f"Read 'init.json' successfully: {init_dict}")

flags = pygame.RESIZABLE | pygame.RESIZABLE | pygame.DOUBLEBUF
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
win_x, win_y = init_dict["win_x"], init_dict["win_y"]
screen = pygame.display.set_mode((win_x, win_y), flags)

clock = pygame.time.Clock()

run = True
show_minimap = True  # Variable to toggle minimap
objects = create_game(screen, file)
# print(objects)
for obj in objects:
    objects[obj].update(file)
repos(objects, file)
while run:
    quit(run)
    repos(objects, file)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        objects["player"].update(file, rotate=5)
    elif keys[pygame.K_d]:
        objects["player"].update(file, rotate=-5)
    if keys[pygame.K_w]:
        for obj in objects:
            if obj != "player":
                rad = math.radians(90 - objects["player"].rotate)
                x = 100 * math.cos(rad)
                y = 100 * math.sin(rad)
                objects[obj].update(file, x=x, y=y)
    elif keys[pygame.K_s]:
        for obj in objects:
            if obj != "player":
                rad = math.radians(90 - (180 + objects["player"].rotate))
                x = 5 * math.cos(rad)
                y = 5 * math.sin(rad)
                objects[obj].update(file, x=x, y=y)

    if keys[pygame.K_m]:
        show_minimap = not show_minimap  # Toggle the minimap

    screen.fill((0, 0, 0))
    for obj in objects:
        if obj != "player":
            objects[obj].update(file)
            objects[obj].draw(screen)

    objects["player"].update(file)
    objects["player"].draw(screen)

    if show_minimap:
        draw_pointers(screen, objects["player"], objects, win_x, win_y)

    pygame.display.flip()
    clock.tick(60)
