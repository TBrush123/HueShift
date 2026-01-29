import pygame
import time
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

    def render(self, screen, delta_time):   
        t1 = time.perf_counter()
        screen.fill((228, 228, 228))
        fill_time = time.perf_counter() - t1
        
        t2 = time.perf_counter()
        self.player.render(screen)
        player_time = time.perf_counter() - t2
        
        t3 = time.perf_counter()
        fps = int(self.game.clock.get_fps())
        fps_text = self.debug_font.render(f"FPS: {fps}", True, (0, 0, 0))
        fill_text = self.debug_font.render(f"Fill: {fill_time*1000:.2f}ms", True, (0, 0, 0))
        player_text = self.debug_font.render(f"Player: {player_time*1000:.2f}ms", True, (0, 0, 0))
        screen.blit(fps_text, (10, 10))
        screen.blit(fill_text, (10, 35))
        screen.blit(player_text, (10, 60))
        debug_time = time.perf_counter() - t3
        debug_text = self.debug_font.render(f"Debug: {debug_time*1000:.2f}ms", True, (0, 0, 0))
        screen.blit(debug_text, (10, 85))