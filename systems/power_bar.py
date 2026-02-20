import pygame
import math

class PowerBar():
    def __init__(self):
        self.power = 0
        self.color = (255, 0, 0)
        self.border_margin = 2
        self.font = pygame.font.Font(None, 24)
        self.power_level = 1
        self.phantom_power = 0 # To add smooth border
        self.power_multiplier = 1.0

    def Update(self, delta):
        if self.phantom_power != self.power:
            # Speed based on the difference between phantom_power and target power
            difference = abs(self.power - self.phantom_power)
            speed = difference * 2  # Scale the difference to get the speed
            if self.phantom_power < self.power:
                self.phantom_power = min(self.phantom_power + speed * delta, self.power)
            else:
                self.phantom_power = max(self.phantom_power - speed * delta, self.power)
        elif self.power > 0:
            self.power = max(0, self.power - 0.5 * delta) #To not go negative on power.

    def change_color(self, color):
        self.color = color

    def add_power(self, amount=5):
        self.power += amount
        if self.power >= 100:
            self.power = 0
            self.power_up()
    
    def power_up(self):
        self.power_level += 1
        self.power_multiplier = 1 + (self.power_level - 1) * 0.5 # Increase multiplier by 0.5 for each level
        
    def get_power_multiplier(self):
        return self.power_multiplier

    def render(self, screen, left_top, size):
        pygame.draw.rect(screen, self.color, 
                         (int(left_top.x), int(left_top.y),
                          size.x, size.y))
        full_box_width = size.x - self.border_margin * 2
        color_box_percent = self.phantom_power / 100
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