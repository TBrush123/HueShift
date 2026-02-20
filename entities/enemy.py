import random
import pygame
import math
from entities.bullet import Bullet


def spawn_bullet(pos, direction, color):
    """Spawn a bullet at the given position in the given direction"""
    return Bullet(pos, direction, color)


class Enemy:
    def __init__(self, pos, player, color, pattern=0):
        """
        Initialize enemy
        Arguments:
            pos: Starting position
            player: Player object to track for movement and targeting
            pattern: Shooting pattern (0-4)
            color: Enemy color
        """
        self.health = 100
        self.pos = pygame.Vector2(pos)
        self.player = player
        self.color = color
        self.pattern = pattern
        self.radius = 10
        self.speed = 100
        self.shoot_timer = 0
        self.angle_offset = 0  # For rotating patterns
        
        match pattern:
            case 0:
                self.shoot_interval = 0.5  # Omnidirectional
            case 1:
                self.shoot_interval = 0.4  # Cone shots
            case 2:
                self.shoot_interval = 0.3  # Alternating pattern
            case 3:
                self.shoot_interval = 0.2  # Rapid burst
            case 4:
                self.shoot_interval = 0.6  # Spiral pattern
    
    def set_color(self, color):
        self.color = color
    
    def update(self, delta):
        self.shoot_timer += delta
        self.angle_offset += delta
        
        # Move towards player
        if self.player:
            direction = self.player.pos - self.pos
            if direction.length() > 0:
                direction = direction.normalize()
                self.pos += direction * self.speed * delta
        
    def take_damage(self, amount, death_color):
        self.health -= amount * (2 if self.color != death_color else 1)
        print(f"Enemy health: {self.health}")
        if self.health > 0:
            return
        if self.color == death_color:
            for _ in range(random.randint(3, 6)):
                angle = random.uniform(0, 2 * math.pi)
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                spawn_bullet(self.pos + direction * random.uniform(5, 15), pygame.Vector2(0, 0), self.color)
        del self
        
    def get_bullets(self):
        """Get bullets based on the current pattern"""
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            bullets = []
            
            if self.pattern == 0:
                # Pattern 0: Omnidirectional (8 directions)
                bullets = self._pattern_omnidirectional()
            elif self.pattern == 1:
                # Pattern 1: Cone towards player
                bullets = self._pattern_cone()
            elif self.pattern == 2:
                # Pattern 2: Alternating spread
                bullets = self._pattern_alternating()
            elif self.pattern == 3:
                # Pattern 3: Rapid burst towards player
                bullets = self._pattern_burst()
            else:  # pattern == 4
                # Pattern 4: Spiral pattern
                bullets = self._pattern_spiral()
            
            return bullets
        return []
    
    def _pattern_omnidirectional(self):
        """Pattern 0: Shoot in 8 directions"""
        bullets = []
        for i in range(8):
            angle = (2 * math.pi * i) / 8
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            bullets.append(spawn_bullet(self.pos, direction, self.color))
        return bullets
    
    def _pattern_cone(self):
        """Pattern 1: Shoot cone towards player"""
        bullets = []
        direction_to_player = self.player.pos - self.pos
        if direction_to_player.length() > 0:
            direction_to_player = direction_to_player.normalize()
            base_angle = math.atan2(direction_to_player.y, direction_to_player.x)
            
            # 3 bullets in a cone
            for i in range(3):
                offset = (i - 1) * 0.3  # Spread cone
                angle = base_angle + offset
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                bullets.append(spawn_bullet(self.pos, direction, self.color))
        return bullets
    
    def _pattern_alternating(self):
        """Pattern 2: Alternating spread pattern"""
        bullets = []
        direction_to_player = self.player.pos - self.pos
        if direction_to_player.length() > 0:
            direction_to_player = direction_to_player.normalize()
            base_angle = math.atan2(direction_to_player.y, direction_to_player.x)
            
            # 5 bullets with alternating spread
            for i in range(5):
                offset = (i - 2) * 0.4
                angle = base_angle + offset
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                bullets.append(spawn_bullet(self.pos, direction, self.color))
        return bullets
    
    def _pattern_burst(self):
        """Pattern 3: Rapid burst directly at player"""
        bullets = []
        direction_to_player = self.player.pos - self.pos
        if direction_to_player.length() > 0:
            direction_to_player = direction_to_player.normalize()
            # Single bullet, but fires very frequently due to low shoot_interval
            bullets.append(spawn_bullet(self.pos, direction_to_player, self.color))
        return bullets
    
    def _pattern_spiral(self):
        """Pattern 4: Spiral pattern that rotates"""
        bullets = []
        num_bullets = 6
        for i in range(num_bullets):
            angle = (2 * math.pi * i) / num_bullets + self.angle_offset * 2
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            bullets.append(spawn_bullet(self.pos, direction, self.color))
        return bullets
    
    def render(self, screen):
        # Draw enemy
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
