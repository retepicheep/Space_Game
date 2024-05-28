import pygame
from space_game import handle_json, create_game, quit, repos, draw_minimap
import math

pygame.init()

init_dict = handle_json("init.json", "read")
# if init_dict is None:
#     print("Failed to read 'init.json'.")
# else:
#     print(f"Read 'init.json' successfully: {init_dict}")

win_x, win_y = init_dict["win_x"], init_dict["win_y"]
screen = pygame.display.set_mode((win_x, win_y), pygame.RESIZABLE)

clock = pygame.time.Clock()

run = True
show_minimap = False  # Variable to toggle minimap
objects = create_game(screen)
for obj in objects:
    objects[obj].update()
repos(objects)
while run:
    quit(run)
    repos(objects)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        objects["player"].update(rotate=5)
    elif keys[pygame.K_d]:
        objects["player"].update(rotate=-5)
    if keys[pygame.K_w]:
        for obj in objects:
            if obj != "player":
                rad = math.radians(90 - objects["player"].rotate)
                x = 5 * math.cos(rad)
                y = 5 * math.sin(rad)
                objects[obj].update(x=x, y=y)
    elif keys[pygame.K_s]:
        for obj in objects:
            if obj != "player":
                rad = math.radians(90 - (180 + objects["player"].rotate))
                x = 5 * math.cos(rad)
                y = 5 * math.sin(rad)
                objects[obj].update(x=x, y=y)

    if keys[pygame.K_m]:
        show_minimap = not show_minimap  # Toggle the minimap

    screen.fill((0, 0, 0))
    for obj in objects:
        if obj != "player":
            objects[obj].update()
            objects[obj].draw(screen)

    objects["player"].update()
    objects["player"].draw(screen)

    if show_minimap:
        draw_minimap(screen, objects, objects["player"], win_x, win_y, 200, 200, 0.1)

    pygame.display.flip()
    clock.tick(60)
