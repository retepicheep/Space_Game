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
            data["size"] if not isinstance(data["size"], str) else eval(data["size"]),
            data["rotate"],
            data["object_type"],
            data["name"],
            data["sprite"],
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
        keywords=None,
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
        )
        self.sprite = self.original_sprite
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect = self.sprite.get_rect(center=(self.pos_x, self.pos_y))
        self.update_sprite()
        self.fly = fly
        self.path = sprite

        # Add attributes to game_data.json
        self.save_to_json()

    def save_to_json(self):
        attributes = {
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "size": self.size,
            "rotate": self.rotate,
            "object_type": self.object_type,
            "name": self.name,
            "sprite": self.path,  # Assuming you want the sprite path, not the loaded image
            "fly": self.fly,
        }
        # Check and update the game_data.json file with the new attributes if they don't exist
        for key, value in attributes.items():
            existing_value = handle_json(
                "game_data.json", "read", keywords=self.keywords + [key]
            )
            if existing_value is None:
                handle_json(
                    "game_data.json",
                    "update",
                    keywords=self.keywords + [key],
                    update_data=value,
                )

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

    def draw_on_minimap(self, minimap_surface, scale):
        mini_rect = self.rect.copy()
        mini_rect.width = int(mini_rect.width * scale)
        mini_rect.height = int(mini_rect.height * scale)
        mini_rect.center = (int(self.pos_x * scale), int(self.pos_y * scale))
        mini_sprite = pygame.transform.scale(
            self.sprite, (mini_rect.width, mini_rect.height)
        )
        minimap_surface.blit(mini_sprite, mini_rect.topleft)
