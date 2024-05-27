import pygame
from space_game.helpers import handle_json
# import os


class GameObject:
    def game_from_json(game_data):
        player_data = handle_json(game_data, "read", keywords=["player"])

        # print(os.path.abspath(player_data["sprite"]))

        return GameObject(
            player_data["pos_x"],
            player_data["pos_y"],
            eval(player_data["size"]),
            player_data["rotate"],
            player_data["object_type"],
            player_data["name"],
            player_data["sprite"],
        )

    def __init__(
        self,
        pos_x,
        pos_y,
        size,
        rotate,
        object_type,
        name,
        sprite,
    ) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.rotate = rotate
        self.object_type = object_type
        self.name = name
        self.original_sprite = pygame.transform.scale(
            pygame.image.load(sprite), self.size
        )
        self.sprite = self.original_sprite
        self.mask = pygame.mask.from_surface(self.sprite)
        self.update_sprite()

    def update(self, x=0, y=0, rotate=0):
        self.pos_x += x
        self.pos_y += y
        self.rotate += rotate
        self.update_sprite()

        handle_json(
            "game_data.json",
            "update",
            keywords=["player", "pos_x"],
            update_data=self.pos_x,
        )
        handle_json(
            "game_data.json",
            "update",
            keywords=["player", "pos_y"],
            update_data=self.pos_y,
        )
        handle_json(
            "game_data.json",
            "update",
            keywords=["player", "rotate"],
            update_data=self.rotate,
        )

    def update_sprite(self):
        self.sprite = pygame.transform.rotate(self.original_sprite, self.rotate)
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect = self.sprite.get_rect(center=(self.pos_x, self.pos_y))

    def draw(self, screen):
        screen.blit(self.sprite, self.rect.topleft)

    def check_collision(self, other):
        offset = (other.rect.left - self.rect.left, other.rect.top - self.rect.top)
        return self.mask.overlap(other.mask, offset) is not None
