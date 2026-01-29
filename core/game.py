import pygame
from scenes.gameplay import GameplayScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Hue Shift")
        self.clock = pygame.time.Clock()
        self.scene = GameplayScene(self)

    def run(self):
        while True:
            delta = self.clock.tick(60) / 1000.0
            self.scene.handle_events()
            self.scene.update(delta)
            self.scene.render(self.screen, delta)
            pygame.display.flip()
