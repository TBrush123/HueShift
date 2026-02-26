import pygame
import random
import math

class TriangleParticle:
    def __init__(self, pos, color):
        self.pos = pygame.Vector2(pos)
        # velocity random direction
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(100, 200)
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        self.angle = random.uniform(0, 2 * math.pi)
        self.spin = random.uniform(-5, 5)
        self.size = random.uniform(6, 12)
        self.color = color
        self.lifetime = 1.0  # seconds
    
    def update(self, delta):
        self.pos += self.vel * delta
        self.angle += self.spin * delta
        self.lifetime -= delta
    
    def render(self, screen):
        if self.lifetime <= 0:
            return
        # compute triangle points centered on pos
        pts = []
        for i in range(3):
            a = self.angle + i * (2 * math.pi / 3)
            x = self.pos.x + math.cos(a) * self.size
            y = self.pos.y + math.sin(a) * self.size
            pts.append((x, y))
        alpha = int(255 * min(1, self.lifetime / 1.0) * 0.95)
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.polygon(surf, (*self.color, alpha), [(p[0]-self.pos.x+self.size, p[1]-self.pos.y+self.size) for p in pts])
        screen.blit(surf, (self.pos.x - self.size, self.pos.y - self.size))