import random
from entities.enemy import Enemy, ChameleonEnemy
from entities.boss import Boss


class TimerSystem:
    def __init__(self, player, color_system, scoring_system=None):
        # scoring_system optional, used to adjust hp based on multiplier
        """
        Initialize the timer system
        Arguments:
            player: Player object for enemy targeting
            color_system: Color system for enemy colors
        """
        self.player = player
        self.color_system = color_system
        self.scoring_system = scoring_system
        self.total_time = 240  # 4 minutes in seconds
        self.elapsed_time = 0
        self.enemies_spawned = []
        self.boss = None
        self.boss_spawned = False
        self.last_spawn_time = 0
        self.spawn_interval = 0.5  # spawn more frequently
        self.enemy_counter = 0
    
    def update(self, delta_time, alive_enemies):
        """
        Update timer system and spawn enemies
        Arguments:
            delta_time: Time elapsed since last update
            alive_enemies: List of currently alive enemies
        """
        self.elapsed_time += delta_time
        self.last_spawn_time += delta_time
        
        # Spawn enemies at intervals; spawn multiple to increase density
        if self.last_spawn_time >= self.spawn_interval and self.elapsed_time < self.total_time:
            # number of enemies increases with time_progress
            count = 1 + int(self.elapsed_time / 30)  # more every 30s
            for _ in range(count):
                self._spawn_enemy()
            self.last_spawn_time = 0
        
        # Spawn boss when time runs out
        if self.elapsed_time >= self.total_time and not self.boss_spawned:
            self._spawn_boss()
    
    def _spawn_enemy(self):
        """Spawn an enemy based on current time"""
        self.enemy_counter += 1
        
        # Calculate difficulty multipliers based on time
        time_progress = self.elapsed_time / self.total_time  # 0.0 to 1.0
        
        # Enemies should be killable in one shot by opposite-color hits (double damage)
        # but survive a same-color shot.  We'll aim hp around 1.5×base damage,
        # slowly creeping upward over time but never reaching 2×damage.
        damage_est = getattr(self.player, "base_damage", 1)
        time_bonus = time_progress * 0.5  # small growth over whole run
        base_hp = damage_est * 1.5 + time_bonus
        # clamp just below double-damage threshold
        base_hp = min(base_hp, damage_est * 2 - 0.01)
        # include small multiplier bonus if available to track scaling
        if self.scoring_system is not None:
            base_hp += self.scoring_system.multiplier * 0.1
        # clamp again after bonus
        base_hp = min(base_hp, damage_est * 2 - 0.01)
        
        # Speed increases over time: 100 to 160
        speed = 100 + time_progress * 60
        
        # Bullet speed increases over time: 240 to 360
        bullet_speed = 240 + time_progress * 120
        
        # Spawn delay decreases over time
        spawn_delay = max(0.3, 0.8 - time_progress * 0.5)
        
        # Position enemies randomly across the top of the screen
        x_pos = random.randint(100, 1100)
        y_pos = random.randint(80, 150)
        
        color = random.choice([self.color_system.RED, self.color_system.BLUE])
        print(f"Spawning enemy with HP {base_hp:.2f} (color {('RED' if color==self.color_system.RED else 'BLUE')})")
        
        # Determine pattern complexity based on time
        if time_progress < 0.25:
            allowed_patterns = [0]  # Only omnidirectional
        elif time_progress < 0.5:
            allowed_patterns = [0, 1]  # Add cone shots
        elif time_progress < 0.75:
            allowed_patterns = [0, 1, 2]  # Add alternating pattern
        else:
            allowed_patterns = [0, 1, 2, 4]  # Add spiral pattern
        
        pattern = random.choice(allowed_patterns)
        
        # Increase chance of chameleon enemies over time
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
    
    def _spawn_boss(self):
        """Spawn the final boss"""
        self.boss = Boss((600, 150), self.player, self.color_system)
        self.boss_spawned = True
    
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
    
    def is_boss_spawned(self):
        """Check if boss has been spawned"""
        return self.boss_spawned
    
    def is_boss_dead(self):
        """Check if boss is dead"""
        return self.boss is not None and self.boss.health <= 0
    
    def get_boss(self):
        """Get the boss if spawned"""
        return self.boss
    
    def get_enemies(self):
        """Get the enemies spawned"""
        return self.enemies_spawned
    
    def format_time(self, seconds):
        """Format seconds as MM:SS"""
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes}:{secs:02d}"
