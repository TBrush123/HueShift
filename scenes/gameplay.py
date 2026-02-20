import pygame
import math 

from core.scene import Scene
from entities.player import Player
from entities.bullet import Bullet
from entities.enemy import Enemy
from systems.color_system import ColorSystem
from systems.collision_system import CollisionSystem
from systems.power_bar import PowerBar
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
        self.player_bullets = []
        self.power = 1
        self.player_base_damage = 1
        self.power_bar = PowerBar()
        self.enemy = []
        self.enemy = [Enemy((400, 200), self.player, (255,84,78), 4)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.color_system.switch()
                    self.color_texts = []
                    self.power_bar.change_color(self.color_system.current_color())

    def update(self, delta_time):
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
                self.power_bar.add_power()
            else:
                pass
            self.bullets.remove(bullet)
        for bullet in self.player_bullets:
            bullet.update(delta_time)
            for enemy in self.enemy:
                if self.collision_system.circle_hit(enemy, bullet):
                    enemy.take_damage(self.player_base_damage * self.power_bar.get_power_multiplier(), self.player.color)
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
        self.power_bar.Update(delta_time)
        for enemy in self.enemy:
            enemy.update(delta_time)
            new_bullets = enemy.get_bullets()
            self.bullets.extend(new_bullets)
        self.player_bullets.extend(self.player.get_bullets())

    def render(self, screen, delta_time):   
        screen.fill((228, 228, 228))
        self.player.render(screen)
        for bullet in self.bullets:
            bullet.render(screen)
        for bullet in self.player_bullets:
            bullet.render(screen)
        for text in self.color_texts:
            text.render(screen)
        for enemy in self.enemy:
            enemy.render(screen)
        fps_font = pygame.font.Font(None, 36)
        fps_text = fps_font.render(f"FPS: {int(self.game.clock.get_fps())}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 10))
        self.power_bar.render(screen, pygame.Vector2(100, 750),pygame.Vector2(1000, 25))