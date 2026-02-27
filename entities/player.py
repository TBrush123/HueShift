import pygame
from pygame import surface
import systems.color_system
import sys

from entities.player_bullets import PlayerBullet

def shoot_player_bullet(pos, direction, color):
    return PlayerBullet(pos, direction, color)

class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.pos = pygame.Vector2(400, 300)
        self.color = systems.color_system.RED
        self.speed = 300
        self.direction = pygame.Vector2(0, 0)
        # Collision hitbox (smaller) vs visual sprite radius
        self.radius = 12  # collision radius used for hit detection
        self.visual_radius = 30  # visual size for sprites
        # visual sprite box proportions: width : height = 1 : 2
        self.sprite_width = int(self.visual_radius * 2)
        self.sprite_height = int(self.sprite_width * 2)
        # player initially looks left
        self.facing_left = True
        self.t = 0
        self.player_sprites = {"red": {}, "blue": {}}

        try:
            # load and scale sprites to player visual size
            w, h = self.sprite_width, self.sprite_height
            # red sprites
            img = pygame.image.load("./assets/red_idle.png").convert_alpha()
            self.player_sprites["red"]["idle"] = pygame.transform.smoothscale(img, (w, h))
            img = pygame.image.load("./assets/red_walk.png").convert_alpha()
            self.player_sprites["red"]["walk"] = pygame.transform.smoothscale(img, (w, h))
            # blue sprites (optional)
            img = pygame.image.load("./assets/blue_idle.png").convert_alpha()
            self.player_sprites["blue"]["idle"] = pygame.transform.smoothscale(img, (w, h))
            img = pygame.image.load("./assets/blue_walk.png").convert_alpha()
            self.player_sprites["blue"]["walk"] = pygame.transform.smoothscale(img, (w, h))
        except Exception as e:
            print(f"Cannot load player images - {e}")
            # Fall back to a simple surface so game can still run
            w, h = self.sprite_width, self.sprite_height
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            rect = pygame.Rect(0, 0, w, h)
            pygame.draw.rect(surf, (200, 200, 200, 150), rect, border_radius=max(0, w//4))
            # provide fallback for both colors
            self.player_sprites["red"]["idle"] = surf
            self.player_sprites["red"]["walk"] = surf
            self.player_sprites["blue"]["idle"] = surf
            self.player_sprites["blue"]["walk"] = surf

    def update(self, delta_time):
        self.t += delta_time
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a],
                                keys[pygame.K_s] - keys[pygame.K_w])
        if direction.length() > 0:
            direction.normalize_ip()

        moving = direction.length() > 0
        self.pos += direction * self.speed * delta_time

        # update sprite based on movement and current color
        color_key = "red" if self.color == systems.color_system.RED else "blue"
        state = "walk" if moving else "idle"
        # pick sprite if available, otherwise keep previous
        if color_key in self.player_sprites and state in self.player_sprites[color_key]:
            self.image = self.player_sprites[color_key][state].copy()
            # flip sprite horizontally when changing direction
            # only change facing when there's horizontal input
            if direction.x != 0:
                self.facing_left = True if direction.x < 0 else False
            if not self.facing_left:
                try:
                    self.image = pygame.transform.flip(self.image, True, False)
                except Exception:
                    pass
            # apply a small opacity (semi-transparent)
            try:
                self.image.set_alpha(int(255 * 0.95))
            except Exception:
                pass
    
    def get_bullets(self):
        if self.t < 0.05:
            return []
        if not pygame.mouse.get_pressed()[0]:
            return []
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_pos) - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        bullet = shoot_player_bullet(self.pos, direction, self.color)
        self.t = 0
        return [bullet]

    def render(self, screen):   
        if not hasattr(self, 'image') or self.image is None:
            w, h = self.sprite_width, self.sprite_height
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (200, 200, 300, 0), pygame.Rect(0, 0, w*2, h*2), border_radius=max(0, w//4))
            self.image.set_alpha(int(255 * 0.95))

        rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        
        screen.blit(self.image, rect)