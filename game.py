import pygame
from map import *
from consts import *
from objcets import *
from player import *


class Game():
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((W, H))
        self.background = Background()
        pygame.display.set_caption("Space Game")

    def run(self):
        player = Player(1)
        planets = pygame.sprite.Group()
        self.background.generate(self.surface, planets, 11, Planet)
        player.draw(self.surface, "forward")
        objects = self.background.objects
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.surface.fill("#000000")
                for object in objects:
                    object.y += 2
                    self.background.build(object)
                    player.draw(self.surface, "forward")
            if keys[pygame.K_DOWN]:
                self.surface.fill("#000000")
                for object in objects:
                    object.y -= 2
                    self.background.build(object)
                    player.draw(self.surface, "back")
            if keys[pygame.K_RIGHT]:
                self.surface.fill("#000000")
                for object in objects:
                    object.x -= 2
                    self.background.build(object)
                    player.draw(self.surface, "right")
            if keys[pygame.K_LEFT]:
                self.surface.fill("#000000")
                for object in objects:
                    object.x += 2
                    self.background.build(object)
                    player.draw(self.surface, "left")
            if keys[pygame.K_l]:
                if player.collided(objects):
                    pass

            pygame.display.update()


game = Game()
game.run()
