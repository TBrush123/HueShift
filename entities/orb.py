import pygame
import math


class Orb:
    def __init__(self, pos, color_system, orb_type="point"):
        """
        Initialize an orb that can be absorbed by the player
        Arguments:
            pos: Spawn position
            color_system: Color system for current color
            orb_type: Type of orb (point, multiplier, health)
        """
        self.pos = pygame.Vector2(pos)
        self.radius = 6
        self.lifetime = 0
        self.max_lifetime = 8.0  # Disappear after 8 seconds
        self.orb_type = orb_type
        self.float_height = 0
        self.float_speed = 2.0  # Speed of floating animation
        self.collected = False
        self.color_system = color_system
        self.color = color_system.current_color()
    
    def update(self, delta_time, target_pos=None):
        """
        Update orb state
        Arguments:
            delta_time: Time since last update
            target_pos: Player position for homing effect when close
        """
        if self.collected:
            return
        
        self.lifetime += delta_time
        self.float_height = math.sin(self.lifetime * self.float_speed) * 5
        
        # Disappear if lifetime exceeded
        if self.lifetime > self.max_lifetime:
            self.collected = True
            return
        
        # Home towards player if close
        if target_pos:
            distance = (target_pos - self.pos).length()
            if distance < 200:  # Attraction range
                direction = target_pos - self.pos
                if direction.length() > 0:
                    direction = direction.normalize()
                    # Increase speed as player gets closer
                    speed = 100 + (200 - distance) * 2
                    self.pos += direction * speed * delta_time
    
    def render(self, screen):
        """Render the orb with floating animation"""
        if self.collected:
            return
        
        # Calculate alpha based on remaining lifetime (5% more transparent)
        base_alpha = int(255 * 0.95 * (1 - self.lifetime / self.max_lifetime))
        
        # Draw main circle
        pygame.draw.circle(screen, self.color, 
                          (int(self.pos.x), int(self.pos.y - self.float_height)), 
                          self.radius)
        
        # Draw glow effect
        if self.lifetime < 7.0:  # Glow only until near end
            glow_radius = int(self.radius * 1.5)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.color, int(base_alpha // 3)), 
                              (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, 
                       (int(self.pos.x) - glow_radius, 
                        int(self.pos.y - self.float_height) - glow_radius))
