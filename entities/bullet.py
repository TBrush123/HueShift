import pygame

class Bullet():
    def __init__(self, pos, dir, color):
        self.pos = pygame.Vector2(pos)
        self.speed = 600
        self.vel = pygame.Vector2(dir) * self.speed
        self.color = color
        self.radius = 6
    
    def update(self, delta):
        self.pos += self.vel * delta
        if abs(self.pos.x) > 1500 or abs(self.pos.y) > 1500:
            del self

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)