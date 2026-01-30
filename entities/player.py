import pygame

class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.pos = pygame.Vector2(400, 300)
        self.color = (255, 0, 0)
        self.speed = 300
        self.direction = pygame.Vector2(0, 0)
        self.radius = 20

    def update(self, delta_time):
        keys = pygame.key.get_pressed()

        direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a],
                                keys[pygame.K_s] - keys[pygame.K_w])
        if direction.length() > 0:
            direction.normalize_ip()

        self.pos += direction * self.speed * delta_time

    def render(self, screen):   
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)