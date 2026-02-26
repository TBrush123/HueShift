import pygame
import math
import random
from entities.bullet import Bullet


def spawn_bullet(pos, direction, color):
    """Spawn a bullet at the given position in the given direction"""
    return Bullet(pos, direction, color)


class Boss:
    def __init__(self, pos, player, color_system):
        """
        Initialize the final boss
        Arguments:
            pos: Starting position (center)
            player: Player object to track
            color_system: Color system for colors
        """
        self.pos = pygame.Vector2(pos)
        self.player = player
        self.color_system = color_system
        self.radius = 40
        self.speed = 60
        self.health = 500
        self.max_health = 500
        
        # Phase management
        self.phase = 1  # Phase 1: Spawning, Phase 2: Fighting
        self.phase_timer = 0
        self.phase_duration = 15.0  # 15 seconds per phase
        
        # Shooting
        self.shoot_timer = 0
        self.shoot_interval = 0.3
        
        # Spawning
        self.spawn_timer = 0
        self.spawn_interval = 2.0  # Spawn minion every 2 seconds in phase 1
        
        # Movement pattern
        self.move_timer = 0
        self.move_pattern = 0  # For different movement patterns
        
        # Rendering
        self.spawn_delay = 0
        self.is_spawning = False
    
    def update(self, delta):
        """Update boss state"""
        self.phase_timer += delta
        self.move_timer += delta
        self.shoot_timer += delta
        self.spawn_timer += delta
        
        # Check phase transition
        if self.phase_timer >= self.phase_duration:
            self.phase = 2 if self.phase == 1 else 1
            self.phase_timer = 0
        
        # Movement - circular pattern in phase 1, erratic in phase 2
        if self.phase == 1:
            # Circular movement around center
            angle = self.move_timer * 0.5
            center = pygame.Vector2(600, 300)
            self.pos = center + pygame.Vector2(math.cos(angle), math.sin(angle)) * 150
        else:
            # Phase 2: Move towards player but erratically
            direction = self.player.pos - self.pos
            if direction.length() > 0:
                direction = direction.normalize()
                # Add some randomness
                angle_offset = math.sin(self.move_timer * 2) * 0.3
                rotated = pygame.Vector2(
                    direction.x * math.cos(angle_offset) - direction.y * math.sin(angle_offset),
                    direction.x * math.sin(angle_offset) + direction.y * math.cos(angle_offset)
                )
                self.pos += rotated * self.speed * delta
    
    def get_bullets(self):
        """Generate boss bullets"""
        bullets = []
        
        if self.phase == 1:
            # Phase 1: Minimal shooting
            if self.shoot_timer >= self.shoot_interval * 2:
                self.shoot_timer = 0
                # Shoot in 4 directions
                for i in range(4):
                    angle = (2 * math.pi * i) / 4
                    direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                    bullets.append(spawn_bullet(self.pos, direction, self.color_system.RED))
        else:
            # Phase 2: Heavy shooting
            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0
                
                # Shoot towards player
                direction_to_player = self.player.pos - self.pos
                if direction_to_player.length() > 0:
                    direction_to_player = direction_to_player.normalize()
                    base_angle = math.atan2(direction_to_player.y, direction_to_player.x)
                    
                    # 8 bullets in a spread towards player
                    for i in range(8):
                        offset = (i - 3.5) * 0.3
                        angle = base_angle + offset
                        direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                        color = self.color_system.RED if self.pos.x > 600 else self.color_system.BLUE
                        bullets.append(spawn_bullet(self.pos, direction, color))
        
        return bullets
    
    def should_spawn_minion(self):
        """Check if boss should spawn a minion (phase 1 only)"""
        if self.phase == 1 and self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            return True
        return False
    
    def take_damage(self, amount, death_color):
        """
        Take damage and return if dead
        Arguments:
            amount: Damage amount
            death_color: Color that dealt the damage
        """
        # Boss takes full damage from any color
        self.health -= amount
        
        if self.health <= 0:
            return True  # Boss is dead
        return False
    
    def render(self, screen):
        """Render the boss with split coloring"""
        # Left half - BLUE
        # Draw left semicircle in blue
        left_color = self.color_system.BLUE
        pygame.draw.circle(screen, left_color, 
                          (int(self.pos.x - self.radius // 2), int(self.pos.y)), 
                          self.radius // 2)
        
        # Right half - RED
        right_color = self.color_system.RED
        pygame.draw.circle(screen, right_color, 
                          (int(self.pos.x + self.radius // 2), int(self.pos.y)), 
                          self.radius // 2)
        
        # Draw border
        pygame.draw.circle(screen, (0, 0, 0), (int(self.pos.x), int(self.pos.y)), self.radius, 3)
        
        # Draw health bar above boss
        bar_width = 120
        bar_height = 15
        bar_x = self.pos.x - bar_width // 2
        bar_y = self.pos.y - self.radius - 30
        
        # Background
        pygame.draw.rect(screen, (100, 100, 100), (int(bar_x), int(bar_y), bar_width, bar_height))
        
        # Health fill
        health_percent = self.health / self.max_health
        pygame.draw.rect(screen, (0, 255, 0), 
                        (int(bar_x), int(bar_y), bar_width * health_percent, bar_height))
        
        # Border
        pygame.draw.rect(screen, (0, 0, 0), (int(bar_x), int(bar_y), bar_width, bar_height), 2)
        
        # Phase indicator
        phase_font = pygame.font.Font(None, 24)
        phase_text = phase_font.render(f"Phase {self.phase}", True, (0, 0, 0))
        screen.blit(phase_text, (int(self.pos.x - 40), int(self.pos.y - 10)))
