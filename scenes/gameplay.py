import pygame
from core.scene import Scene
from entities.player import Player

class GameplayScene(Scene):
    def __init__(self, game):
        self.game = game
        self.player = Player("Goat", 300)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self, delta_time):
        self.player.update(delta_time)

    def render(self, screen):   
        screen.fill((228, 228, 228))
        self.player.render(screen)
        