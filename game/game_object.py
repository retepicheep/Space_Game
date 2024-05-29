import pygame
from game.helpers import handle_json
# import os


class GameObject:
    def game_from_json(game_data, keywords):
        data = handle_json(game_data, "read", keywords=keywords)

        # print(os.path.abspath(data["sprite"]))

        return GameObject(
            data["pos_x"],
            data["pos_y"],
            data["size"] if not isinstance(data["size"], str) else eval(data["size"]),
            data["rotate"],
            data["object_type"],
            data["name"],
            data["sprite"],
            data["speed"],
            data["keywords"],
            data["fly"],
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
        speed,
        keywords,
        fly=False,
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
        ).convert_alpha()
        self.sprite = self.original_sprite
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect = self.sprite.get_rect(center=(self.pos_x, self.pos_y))
        self.update_sprite()
        self.fly = fly
        self.path = sprite
        self.speed = speed

    def update(self, file, x=0, y=0, rotate=0):
        self.pos_x += x
        self.pos_y += y
        self.rotate += rotate
        self.rect.center = (self.pos_x, self.pos_y)
        self.update_sprite()

        handle_json(
            file,
            "update",
            keywords=self.keywords + ["pos_x"],
            update_data=self.pos_x,
        )
        handle_json(
            file,
            "update",
            keywords=self.keywords + ["pos_y"],
            update_data=self.pos_y,
        )
        handle_json(
            file,
            "update",
            keywords=self.keywords + ["rotate"],
            update_data=self.rotate,
        )

    def update_sprite(self):
        self.sprite = pygame.transform.rotate(self.original_sprite, self.rotate)
        self.rect = self.sprite.get_rect(center=(self.pos_x, self.pos_y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, screen):
        if self.is_visible(screen.get_width(), screen.get_height()):
            screen.blit(self.sprite, self.rect.topleft)

    def check_collision(self, other) -> bool:
        offset = (other.rect.left - self.rect.left, other.rect.top - self.rect.top)
        return self.mask.overlap(other.mask, offset) is not None

    def is_visible(self, screen_width, screen_height, margin=100):
        return (
            self.pos_x + self.rect.width + margin > 0
            and self.pos_x - margin < screen_width
            and self.pos_y + self.rect.height + margin > 0
            and self.pos_y - margin < screen_height
        )
