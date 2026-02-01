import pygame
import math

class PowerBar():
    def __init__(self):
        self.power = 0
        self.color = (255, 0, 0)
        self.border_margin = 5
        self.font = pygame.font.Font(None, 18)

    def Update(self, delta):
        if self.power <= 0:
            return
        self.power = max(0, self.power - 0.5 * delta) #To not go negative on power.

    def change_color(self, color):
        self.color = color

    def add_power(self, amount=5):
        self.power += amount
    
    def render(self, screen, left_top, size):
        pygame.draw.rect(screen, self.color, 
                         (int(left_top.x), int(left_top.y),
                          size.x, size.y))
        full_box_width = size.x - self.border_margin * 2
        color_box_percent = self.power / 100
        color_box_width = int(color_box_percent * full_box_width) #First half of the progress bar 
        black_box_width = int((1 - color_box_percent) * full_box_width) #Other half of the progress bar

        pygame.draw.rect(screen, self.color, 
                         (int(left_top.x) + self.border_margin, int(left_top.y) + self.border_margin,
                          color_box_width, size.y - self.border_margin * 2))
        pygame.draw.rect(screen, (0, 0, 0), (left_top.x + self.border_margin + color_box_width, left_top.y + self.border_margin,
                                             black_box_width, size.y - self.border_margin * 2))
        power_text = self.font.render(f"{math.ceil(self.power)}%", True, (255, 255, 255)) #Content of the power text
        text_rect = power_text.get_rect()
        text_rect.center = ((left_top.x * 2 + size.x) / 2, (left_top.y * 2 + size.y) / 2) #Text position
        screen.blit(power_text, text_rect)