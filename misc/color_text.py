import pygame
import systems.color_system

class ColorText():
    def __init__(self, index, color):
        self.font = pygame.font.Font(None, 108)
        self.color = color
        self.text = '/ RED /' if color == systems.color_system.COLORS[0] else '/ BLUE /'
        self.text_bound = 25 * len(self.text)
        self.pos = pygame.Vector2(-(2-index) * self.text_bound, (2 - index) * self.text_bound)
        self.text_speed = 160
        self.centre_pos = pygame.Vector2(150, 150)
    
    def change_color(self, color):
        self.text = 'RED //' if color == (255, 0, 0) else 'BLUE //'
        self.text_bound = 27 * len(self.text)
        self.color = color

    def update(self, delta):
        if self.pos.y < -self.text_bound * 2:
            self.pos = pygame.Vector2(-self.text_bound * 2, self.text_bound * 2) 
        self.pos += pygame.Vector2(self.text_speed, -self.text_speed) * delta

    def render(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        # Apply 95% opacity
        text_surface.set_alpha(int(255 * 0.95))
        angled_text = pygame.transform.rotate(text_surface, 45)
        rect = angled_text.get_rect(center=self.pos + self.centre_pos)
        screen.blit(angled_text, rect)
