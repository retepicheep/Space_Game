import pygame
from space_game.helpers import handle_json
# import os


class GameObject:
    def game_from_json(game_data, keywords):
        data = handle_json(game_data, "read", keywords=keywords)

        # print(os.path.abspath(data["sprite"]))

        return GameObject(
            data["pos_x"],
            data["pos_y"],
            eval(data["size"]),
            data["rotate"],
            data["object_type"],
            data["name"],
            data["sprite"],
            data["keywords"],
        )

    def __init__(
        self, pos_x, pos_y, size, rotate, object_type, name, sprite, keywords=None
    ) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.rotate = rotate
        self.object_type = object_type
        self.name = name
        self.keywords = [keywords] if isinstance(keywords, str) else keywords
        self.original_sprite = pygame.transform.scale(
            pygame.image.load(sprite), self.size
        )
        self.sprite = self.original_sprite
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect = self.sprite.get_rect(center=(self.pos_x, self.pos_y))
        self.update_sprite()

    def update(self, x=0, y=0, rotate=0):
        self.pos_x += x
        self.pos_y += y
        self.rotate += rotate
        self.rect.center = (self.pos_x, self.pos_y)
        self.update_sprite()

        handle_json(
            "game_data.json",
            "update",
            keywords=self.keywords + ["pos_x"],
            update_data=self.pos_x,
        )
        handle_json(
            "game_data.json",
            "update",
            keywords=self.keywords + ["pos_y"],
            update_data=self.pos_y,
        )
        handle_json(
            "game_data.json",
            "update",
            keywords=self.keywords + ["rotate"],
            update_data=self.rotate,
        )

    def update_sprite(self):
        self.sprite = pygame.transform.rotate(self.original_sprite, self.rotate)
        self.rect = self.sprite.get_rect(center=(self.pos_x, self.pos_y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, screen):
        screen.blit(self.sprite, self.rect.center)

    def check_collision(self, other) -> bool:
        offset = (other.rect.left - self.rect.left, other.rect.top - self.rect.top)
        return self.mask.overlap(other.mask, offset) is not None
