import pygame
import math 

from core.scene import Scene
from entities.player import Player
from entities.bullet import Bullet
from systems.color_system import ColorSystem
from systems.collision_system import CollisionSystem
from misc.color_text import ColorText

class GameplayScene(Scene):
    def __init__(self, game):
        self.game = game
        self.player = Player("Goat", 300)
        self.color_system = ColorSystem()
        current_color = self.color_system.current_color()
        self.color_texts = [ColorText(0, current_color), ColorText(1, current_color), ColorText(2, current_color), ColorText(3, current_color)]
        self.collision_system = CollisionSystem()
        self.bullets = []
        self.t = 0
        self.bullet_test = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.color_system.switch()
                    self.color_texts = []

    def update(self, delta_time):

        if self.t >= 1:
            self.bullets.append(Bullet((800, 400), (-1, 0), (255, 0, 0) if self.bullet_test else (0, 0, 255)))
            self.t = 0
            self.bullet_test = not self.bullet_test

        self.player.color = self.color_system.current_color()
        self.player.update(delta_time)
        if not self.color_texts:
            current_color = self.color_system.current_color()
            self.color_texts = [ColorText(0, current_color), ColorText(1, current_color), ColorText(2, current_color), ColorText(3, current_color)]
        for text in self.color_texts:
            text.update(delta_time) 
        for bullet in self.bullets:
            bullet.update(delta_time)
            if not self.collision_system.circle_hit(self.player, bullet):
                continue
            elif self.player.color == bullet.color:
                print("Absorbed!")
            else:
                print("Dead!")
            self.bullets.remove(bullet)
        self.t += delta_time

    def render(self, screen, delta_time):   
        screen.fill((228, 228, 228))
        self.player.render(screen)
        for bullet in self.bullets:
            bullet.render(screen)
        for text in self.color_texts:
            text.render(screen)

        fps_font = pygame.font.Font(None, 36)
        fps_text = fps_font.render(f"FPS: {int(self.game.clock.get_fps())}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 10))