import pygame
from entities.player_bullets import PlayerBullet

def shoot_player_bullet(pos, direction, color):
    return PlayerBullet(pos, direction, color)

class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.pos = pygame.Vector2(400, 300)
        self.color = (255, 0, 0)
        self.speed = 300
        self.direction = pygame.Vector2(0, 0)
        self.radius = 20
        self.t = 0

    def update(self, delta_time):
        self.t += delta_time
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a],
                                keys[pygame.K_s] - keys[pygame.K_w])
        if direction.length() > 0:
            direction.normalize_ip()

        self.pos += direction * self.speed * delta_time
    
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
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)