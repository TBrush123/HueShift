import pygame
from scenes.main_menu import MainMenuScene
from systems.color_system import ColorSystem

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Hue Shift")
        self.clock = pygame.time.Clock()
        # start at the main menu
        self.scene = MainMenuScene(self)
        self.color_system = ColorSystem()

    def run(self):
        while True:
            delta = self.clock.tick(60) / 1000.0
            self.scene.handle_events()
            self.scene.update(delta)
            self.scene.render(self.screen, delta)
            pygame.display.flip()
