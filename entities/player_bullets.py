import pygame
import math

class PlayerBullet():
    def __init__(self, pos, dir, color):
        self.pos = pygame.Vector2(pos)
        self.speed = 600
        self.vel = pygame.Vector2(dir) * self.speed
        self.color = color
        self.radius = 20
        self.bullet_speed = 3
    
    def update(self, delta):
        self.pos += self.vel * delta * self.bullet_speed
        if abs(self.pos.x) > 1500 or abs(self.pos.y) > 1500:
            del self

    def render(self, screen):
        # draw triangle pointing along velocity direction
        angle = math.atan2(self.vel.y, self.vel.x)
        points = [
            (self.pos.x + math.cos(angle) * self.radius, self.pos.y + math.sin(angle) * self.radius),
            (self.pos.x + math.cos(angle + 2.5) * self.radius, self.pos.y + math.sin(angle + 2.5) * self.radius),
            (self.pos.x + math.cos(angle - 2.5) * self.radius, self.pos.y + math.sin(angle - 2.5) * self.radius),
        ]
        pygame.draw.polygon(screen, (*self.color, int(255 * 0.95)), points)
