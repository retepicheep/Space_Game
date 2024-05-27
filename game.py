import pygame
from space_game import handle_json, create_game, quit

pygame.init()

init_dict = handle_json("init.json", "read")
# if init_dict is None:
#     print("Failed to read 'init.json'.")
# else:
#     print(f"Read 'init.json' successfully: {init_dict}")

win_x, win_y = init_dict["win_x"], init_dict["win_y"]
screen = pygame.display.set_mode((win_x, win_y))

clock = pygame.time.Clock()

run = True
objects = create_game(screen)
while run:
    quit(run)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        objects["player"].update(rotate=5)
    elif keys[pygame.K_d]:
        objects["player"].update(rotate=-5)
    clock.tick(60)

    screen.fill((0, 0, 0))
    for obj in objects:
        objects[obj].draw(screen)
    pygame.display.flip()
    clock.tick(60)
