import random
import pygame
import math
from entities.bullet import Bullet


def spawn_bullet(pos, direction, color, speed=None):
    """Spawn a bullet at the given position in the given direction.

    The optional `speed` argument allows callers to reduce the bullet velocity
    for easier waves (new players).  When not provided the bullet will use
    whatever default speed is defined in the Bullet class (600).
    """
    b = Bullet(pos, direction, color)
    if speed is not None:
        b.speed = speed
        b.vel = pygame.Vector2(direction) * speed
    return b


class Enemy:
    def __init__(self, pos, player, color, pattern=0, health=50,
                 spawn_delay=0.5, color_system=None, bullet_speed=None):
        """
        Initialize enemy
        Arguments:
            pos: Starting position
            player: Player object to track for movement and targeting
            pattern: Shooting pattern (0-4)
            color: Enemy color
            health: Enemy health (default: 50)
            spawn_delay: Delay before enemy becomes active (default: 0.5 seconds)
            color_system: Color system for tracking game state
            bullet_speed: If provided, override the default bullet speed.  This
                makes it easy to slow down projectiles on early waves.
        """
        self.health = health
        self.max_health = health
        self.pos = pygame.Vector2(pos)
        self.player = player
        self.color = color
        self.pattern = pattern
        self.radius = 24
        self.speed = 100
        self.bullet_speed = bullet_speed  # may be None, meaning default
        self.shoot_timer = 0
        self.angle_offset = 0  # For rotating patterns
        self.spawn_delay = spawn_delay
        self.spawn_timer = 0
        self.is_spawning = True
        self.color_system = color_system
        # visual flash when hit
        self.flash_timer = 0
        
        # choose initial shoot interval based on pattern
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
        # Handle spawn animation
        if self.is_spawning:
            self.spawn_timer += delta
            if self.spawn_timer >= self.spawn_delay:
                self.is_spawning = False
                self.spawn_timer = 0
            return  # Don't update position or shoot while spawning
        
        self.shoot_timer += delta
        self.angle_offset += delta
        
        # Move towards player, with a spiral effect for basic enemies
        if self.player:
            direction = self.player.pos - self.pos
            if direction.length() > 0:
                direction = direction.normalize()
                # basic enemies (pattern 0) spiral inwards
                if self.pattern == 0:
                    # add a small perpendicular component that oscillates
                    perp = pygame.Vector2(-direction.y, direction.x)
                    spiral_strength = 0.5  # adjust for spiral tightness
                    direction = (direction + perp * math.sin(self.angle_offset * 5) * spiral_strength).normalize()
                self.pos += direction * self.speed * delta
        # decrement flash timer
        if self.flash_timer > 0:
            self.flash_timer -= delta
        
    def take_damage(self, amount, death_color):
        self.health -= amount * (2 if self.color != death_color else 1)
        print(f"Enemy health: {self.health}")
        # trigger flash when hit but not dead
        if self.health > 0:
            self.flash_timer = 0.2
        bullets = []
        if self.health > 0:
            return None, bullets  # Alive, no bullets
        
        # enemy is dead - if killed by matching color, shoot death bullets
        if self.color == death_color:
            # Generate spread of bullets in their color
            for i in range(8):
                angle = (2 * math.pi * i) / 8
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                bullets.append(spawn_bullet(self.pos, direction, self.color, self.bullet_speed))
        
        return self, bullets
    
    def get_bullets(self):
        """Get bullets based on the current pattern"""
        if self.is_spawning:
            return []  # Don't shoot while spawning
        # only shoot if player and enemy share color
        if self.player and self.player.color != self.color:
            return []
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            bullets = []
            
            if self.pattern == 0:
                #floating guys (no bullets)
                bullets = []
            elif self.pattern == 1:
                bullets = self._pattern_cone()
            elif self.pattern == 2:
                bullets = self._pattern_alternating()
            elif self.pattern == 3:
                bullets = self._pattern_burst()
            else:  # pattern == 4
                bullets = self._pattern_spiral()
            
            return bullets
        return []
    
    def _pattern_omnidirectional(self):
        """Pattern 0: Shoot in 8 directions"""
        bullets = []
        for i in range(8):
            angle = (2 * math.pi * i) / 8
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            bullets.append(spawn_bullet(self.pos, direction, self.color, self.bullet_speed))
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
                bullets.append(spawn_bullet(self.pos, direction, self.color, self.bullet_speed))
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
                bullets.append(spawn_bullet(self.pos, direction, self.color, self.bullet_speed))
        return bullets
    
    def _pattern_burst(self):
        """Pattern 3: Rapid burst directly at player"""
        bullets = []
        direction_to_player = self.player.pos - self.pos
        if direction_to_player.length() > 0:
            direction_to_player = direction_to_player.normalize()
            # Single bullet, but fires very frequently due to low shoot_interval
            bullets.append(spawn_bullet(self.pos, direction_to_player, self.color, self.bullet_speed))
        return bullets
    
    def _pattern_spiral(self):
        """Pattern 4: Spiral pattern that rotates"""
        bullets = []
        num_bullets = 6
        for i in range(num_bullets):
            angle = (2 * math.pi * i) / num_bullets + self.angle_offset * 2
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            bullets.append(spawn_bullet(self.pos, direction, self.color, self.bullet_speed))
        return bullets
    
    def render(self, screen):
        if self.is_spawning:
            # Draw spawn preview
            # Pulsing effect based on spawn timer
            pulse = self.spawn_timer / self.spawn_delay  # 0 to 1
            preview_radius = int(self.radius * (0.5 + pulse * 0.5))
            preview_alpha = int(120 * 0.95 * (1 - pulse))  # Fades in, 5% more transparent
            
            # Draw expanding circle outline
            outline_surf = pygame.Surface((preview_radius * 2 + 2, preview_radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(outline_surf, (*self.color, int(242)), (preview_radius + 1, preview_radius + 1), preview_radius, 2)
            screen.blit(outline_surf, (int(self.pos.x) - preview_radius - 1, int(self.pos.y) - preview_radius - 1))
            
            # Draw semi-transparent circle
            s = pygame.Surface((preview_radius * 2, preview_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, preview_alpha), (preview_radius, preview_radius), preview_radius)
            screen.blit(s, (int(self.pos.x) - preview_radius, int(self.pos.y) - preview_radius))
        else:
            # Draw fully spawned enemy with 5% more transparency
            # If flashing, make semi-transparent to simulate invisibility
            alpha = int(255 * 0.95)
            if self.flash_timer > 0:
                alpha = int(alpha * 0.3)
            enemy_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(enemy_surf, (*self.color, alpha), (self.radius, self.radius), self.radius)
            screen.blit(enemy_surf, (int(self.pos.x) - self.radius, int(self.pos.y) - self.radius))

class ChameleonEnemy(Enemy):
    """Enemy that changes color to match the player's current color"""
    
    def __init__(self, pos, player, color_system, pattern=0, health=50, spawn_delay=0.5, bullet_speed=None):
        """
        Initialize chameleon enemy
        Arguments:
            pos: Starting position
            player: Player object to track for movement and targeting
            color_system: Color system for syncing with player color
            pattern: Shooting pattern (0-4)
            health: Enemy health (default: 50)
            spawn_delay: Delay before enemy becomes active (default: 0.5 seconds)
            bullet_speed: Optional override for projectile velocity
        """
        # Initialize with a default starting color
        super().__init__(pos, player, color_system.current_color(), pattern, health,
                         spawn_delay, color_system, bullet_speed)
        self.is_chameleon = True
        # make sure the attribute is set in case we change it later
        if bullet_speed is not None:
            self.bullet_speed = bullet_speed
    
    def update(self, delta):
        """Update and sync color with player"""
        # Update color to match player
        self.color = self.player.color
        
        # Call parent update
        super().update(delta)
    
    def take_damage(self, amount, death_color):
        """Override take_damage for chameleon"""
        # Chameleon only takes reduced damage from non-matching colors (since it matches player)
        self.health -= amount * (1 if self.color == death_color else 0.5)
        print(f"Chameleon Enemy health: {self.health}")
        
        bullets = []
        if self.health > 0:
            return None, bullets  # Alive, no bullets
        
        # Chameleon is dead - if killed by matching color, shoot death bullets
        if self.color == death_color:
            # Generate more spread of bullets (chameleon shoots more on death)
            for i in range(12):
                angle = (2 * math.pi * i) / 12
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                bullets.append(spawn_bullet(self.pos, direction, self.color, self.bullet_speed))
        
        return self, bullets