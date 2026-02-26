import pygame
import random
import math

class ColorParticle:
    def __init__(self, pos, color):
        self.pos = pygame.Vector2(pos)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(100, 200)
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        self.color = color
        self.lifetime = 0.5
        self.radius = random.uniform(3, 6)
    
    def update(self, delta):
        self.pos += self.vel * delta
        self.lifetime -= delta
    
    def render(self, screen):
        if self.lifetime <= 0:
            return
        alpha = int(255 * (self.lifetime / 0.5) * 0.95)
        surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (int(self.radius), int(self.radius)), int(self.radius))
        screen.blit(surf, (self.pos.x - self.radius, self.pos.y - self.radius))

class FloatingText:
    def __init__(self, pos, text, color):
        self.pos = pygame.Vector2(pos)
        self.text = text
        self.color = color
        self.lifetime = 1.0
        self.vel = pygame.Vector2(0, -50)  # move upward
        self.font = pygame.font.Font(None, 24)
    
    def update(self, delta):
        self.pos += self.vel * delta
        self.lifetime -= delta
    
    def render(self, screen):
        if self.lifetime <= 0:
            return
        alpha = int(255 * (self.lifetime / 1.0))
        text_surf = self.font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        rect = text_surf.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(text_surf, rect)