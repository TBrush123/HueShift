import pygame


class ScoringSystem:
    def __init__(self):
        """Initialize the scoring system with Ultrakill-style multipliers"""
        self.score = 0
        self.multiplier = 1  # 1x base multiplier
        self.kill_streak = 0
        self.time_since_last_kill = 0
        self.streak_timeout = 5.0  # Reset streak (and multiplier) if no kills for 5 seconds
        self.multiplier_messages = [
            "Dull.",
            "Keep it up!",
            "Not bad!",
            "Great!",
            "On fire!",
            "Unstoppable!",
            "Godlike!",
            "Impossible!",
            "Exalted!",
            "Legendary!"
        ]
        
        self.rank_thresholds = [
            (0, "C"),
            (1000, "B"),
            (3000, "A"),
            (7000, "S"),
            (15000, "SS"),
        ]
    
    def add_kill(self, base_score=100, enemy_hp=50):
        """
        Add a kill to the scoring system
        """
        self.kill_streak += 1
        self.time_since_last_kill = 0
        # multiplier increases by 1 for every kill (equal to kill streak)
        self.multiplier = max(1, self.kill_streak)
        
        # Calculate final score with multiplier and HP bonus
        hp_bonus = int(enemy_hp * 0.5)  # 50% of enemy HP as bonus
        final_score = int((base_score + hp_bonus) * self.multiplier)
        
        self.score += final_score
        return final_score
    
    def update(self, delta_time):
        """Update kill streak timer and decay multibar"""
        self.time_since_last_kill += delta_time
        
        # Reset streak if timeout exceeded
        if self.time_since_last_kill > self.streak_timeout:
            self.kill_streak = 0
            self.multiplier = 1
    
    
    def get_current_rank(self):
        """Get the current rank name based on total score.
        """
        for threshold, rank_name in reversed(self.rank_thresholds):
            if self.score >= threshold:
                return rank_name
        return ""
    
    def get_score(self):
        """Get current total score"""
        return self.score
    
    def get_multiplier(self):
        """Get current multiplier"""
        return self.multiplier

    def get_multiplier_message(self):
        """Get the current message based on multiplier (every 10x)"""
        idx = min(len(self.multiplier_messages) - 1, self.multiplier // 10)
        return self.multiplier_messages[int(idx)]
    
    def extend_time(self, amount):
        """Extend the multiplier timeout by reducing time_since_last_kill"""
        self.time_since_last_kill = max(0, self.time_since_last_kill - amount)
    
    def get_kill_streak(self):
        """Get current kill streak"""
        return self.kill_streak
    
    def get_streak_timeout(self):
        """Get current streak timeout in seconds"""
        return self.streak_timeout
    
    def get_time_since_last_kill(self):
        """Get time elapsed since last kill"""
        return self.time_since_last_kill
