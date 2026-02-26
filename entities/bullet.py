import pygame

class Bullet():
    def __init__(self, pos, dir, color):
        self.pos = pygame.Vector2(pos)
        self.speed = 600
        self.vel = pygame.Vector2(dir) * self.speed
        self.color = color
        self.radius = 14
    
    def update(self, delta):
        self.pos += self.vel * delta
        if abs(self.pos.x) > 1500 or abs(self.pos.y) > 1500:
            del self

    def render(self, screen):
        # Create a surface with the bullet color at 95% opacity
        bullet_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(bullet_surf, (*self.color, int(255 * 0.95)), (self.radius, self.radius), self.radius)
        screen.blit(bullet_surf, (int(self.pos.x) - self.radius, int(self.pos.y) - self.radius))