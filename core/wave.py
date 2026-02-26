import random
from entities.enemy import Enemy, ChameleonEnemy
from entities.boss import Boss


class WaveSystem:
    def __init__(self, player, color_system):
        """
        Initialize the wave system
        Arguments:
            player: Player object for enemy targeting
            color_system: Color system for enemy colors
        """
        self.player = player
        self.color_system = color_system
        self.current_wave = 1
        self.total_waves = 11  # 10 regular waves + 1 boss wave
        self.enemies_spawned = []
        self.wave_complete = False
        self.boss = None
        self.spawn_wave(self.current_wave)
    
    def spawn_wave(self, wave_number):
        """
        Spawn enemies for the given wave
        Arguments:
            wave_number: The wave number (1-11)
        """
        self.enemies_spawned = []
        self.wave_complete = False
        self.boss = None
        
        # Wave 11 is the boss wave
        if wave_number == 11:
            self.boss = Boss((600, 150), self.player, self.color_system)
            return
        
        # Calculate enemy count and HP based on wave
        # Keep early waves easier: slightly fewer enemies and slower projectiles
        enemy_count = min(1 + wave_number, 8)
        base_hp = 40 + (wave_number - 1) * 20  # gentler HP curve for beginners

        # Difficulty scaling variables (more forgiving growth)
        speed = 40 + wave_number * 4               # enemies move a bit slower early on
        bullet_speed = 240 + wave_number * 15      # bullets start slower and scale gently
        spawn_delay = max(0.8 - wave_number * 0.02, 0.35)  # give slightly more spawn time
        
        colors = [self.color_system.RED, self.color_system.BLUE]
        
        for i in range(enemy_count):
            # Spread enemies across three columns to avoid tight clustering
            cols = 3
            col_width = 400
            x_pos = 200 + (i % cols) * col_width
            y_pos = 120 + (i // cols) * 110
            
            color = colors[i % len(colors)]

            # Begin with simple patterns and add complexity gradually.
            # Avoid very fast/risky patterns (like rapid burst) in early waves
            if wave_number <= 2:
                allowed = [0]
            elif wave_number <= 5:
                allowed = [0, 1]
            elif wave_number <= 8:
                allowed = [0, 1, 2]
            elif wave_number <= 10:
                # allow spiral but keep rapid burst mostly for later waves
                allowed = [0, 1, 2, 4]
            else:
                allowed = list(range(5))

            pattern = random.choice(allowed)
            hp = base_hp + i * 10  # Increase HP slightly for each enemy in wave
            
            # Spawn chameleon enemies starting from wave 3, ~30% of enemies
            if wave_number >= 3 and random.random() < 0.3:
                enemy = ChameleonEnemy((x_pos, y_pos), self.player, self.color_system, pattern, hp,
                                        spawn_delay=spawn_delay)
            else:
                enemy = Enemy((x_pos, y_pos), self.player, color, pattern, hp,
                              spawn_delay=spawn_delay, color_system=self.color_system,
                              bullet_speed=bullet_speed)
            # apply movement speed after construction so both types get it
            enemy.speed = speed
            enemy.bullet_speed = bullet_speed
            
            self.enemies_spawned.append(enemy)
    
    def update(self, alive_enemies):
        """
        Update wave state based on alive enemies
        Arguments:
            alive_enemies: List of currently alive enemies
        """
        if len(alive_enemies) == 0 and not self.wave_complete:
            self.wave_complete = True
    
    def is_boss_dead(self):
        """Check if boss is dead"""
        return self.boss is not None and self.boss.health <= 0
    
    def get_boss(self):
        """Get the boss if in boss wave"""
        return self.boss
    
    def next_wave(self):
        """Advance to the next wave"""
        if self.current_wave < self.total_waves:
            self.current_wave += 1
            self.spawn_wave(self.current_wave)
            return True
        return False  # Game complete
    
    def is_wave_complete(self):
        """Check if current wave is complete"""
        return self.wave_complete
    
    def is_game_complete(self):
        """Check if all waves are complete"""
        return self.current_wave == self.total_waves and (self.wave_complete or self.is_boss_dead())
    
    def get_current_wave(self):
        """Get current wave number"""
        return self.current_wave
    
    def get_enemies(self):
        """Get the enemies spawned for the current wave"""
        return self.enemies_spawned
