import random
from entities.enemy import Enemy, ChameleonEnemy


class TimerSystem:
    def __init__(self, player, color_system, scoring_system=None):
        """
        Initialize the timer system
        """
        self.player = player
        self.color_system = color_system
        self.scoring_system = scoring_system
        self.total_time = 251  #4 minutes and 11 seconds
        self.elapsed_time = 0
        self.enemies_spawned = []
        self.last_spawn_time = 0
        # spawn interval in seconds (longer makes game less hectic)
        self.spawn_interval = 1.0
        self.enemy_counter = 0
        # boss logic removed; go until time runs out
    
    def update(self, delta_time, alive_enemies):
        """
        Update timer system and spawn enemies
        """
        self.elapsed_time += delta_time
        self.last_spawn_time += delta_time
        
        # Spawn enemies at intervals; ramp up slower to ease difficulty
        if self.last_spawn_time >= self.spawn_interval and self.elapsed_time < self.total_time:
            count = 1 + int(self.elapsed_time / 45)  # additional enemy every 45s instead of 30
            for _ in range(count):
                self._spawn_enemy()
            self.last_spawn_time = 0
        
    def _spawn_enemy(self):
        """Spawn an enemy based on current time"""
        self.enemy_counter += 1
        
        # Calculate difficulty multiplier
        time_progress = self.elapsed_time / self.total_time  # 0.0 to 1.0
        
        # Increase base HP
        damage_est = getattr(self.player, "base_damage", 1)
        time_bonus = time_progress * 1.0  # increased growth
        base_hp = damage_est * 2.5 + time_bonus
        base_hp = min(base_hp, damage_est * 3 - 0.01)
        if self.scoring_system is not None:
            base_hp += self.scoring_system.multiplier * 0.2
        base_hp = min(base_hp, damage_est * 3 - 0.01)
        
        #increase enemy speed
        speed = 100 + time_progress * 60
        
        # increase bullet speed after time (overall lower growth)
        bullet_speed = 200 + time_progress * 80
        
        spawn_delay = max(0.3, 0.8 - time_progress * 0.5)
        
        # Random spawn
        x_pos = random.randint(100, 1100)
        y_pos = random.randint(80, 150)
        
        color = random.choice([self.color_system.RED, self.color_system.BLUE])
        print(f"Spawning enemy with HP {base_hp:.2f} (color {('RED' if color==self.color_system.RED else 'BLUE')})")
        
        if time_progress < 0.25:
            allowed_patterns = [0]  # Only basic
        elif time_progress < 0.5:
            allowed_patterns = [0, 1]  # Add cone shots
        elif time_progress < 0.75:
            allowed_patterns = [0, 1, 2]  # Add alternating pattern
        else:
            allowed_patterns = [0, 1, 2, 4]  # Add spiral pattern
        
        pattern = random.choice(allowed_patterns)
        chameleon_chance = min(0.5, time_progress * 0.5)  # Up to 50% chance
        
        # adjust hp if enemy color matches player at spawn
        hp = int(base_hp * (2 if color == self.player.color else 1))
        
        if random.random() < chameleon_chance:
            enemy = ChameleonEnemy(
                (x_pos, y_pos), 
                self.player, 
                self.color_system, 
                pattern, 
                hp,
                spawn_delay=spawn_delay
            )
        else:
            enemy = Enemy(
                (x_pos, y_pos), 
                self.player, 
                color, 
                pattern, 
                hp,
                spawn_delay=spawn_delay, 
                color_system=self.color_system,
                bullet_speed=int(bullet_speed)
            )
        
        enemy.speed = speed
        enemy.bullet_speed = int(bullet_speed)
        
        self.enemies_spawned.append(enemy)
    
    
    def get_elapsed_time(self):
        """Get elapsed time in seconds"""
        return self.elapsed_time
    
    def get_remaining_time(self):
        """Get remaining time in seconds"""
        return max(0, self.total_time - self.elapsed_time)
    
    def get_time_progress(self):
        """Get time progress as percentage (0.0 to 1.0)"""
        return min(1.0, self.elapsed_time / self.total_time)
    
    def is_time_up(self):
        """Check if time has run out"""
        return self.elapsed_time >= self.total_time
    
    
    
    
    def get_enemies(self):
        """Get the enemies spawned"""
        return self.enemies_spawned
    
    def format_time(self, seconds):
        """Format seconds as MM:SS"""
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes}:{secs:02d}"
