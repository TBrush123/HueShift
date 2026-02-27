import pygame
import math
import random 

from core.scene import Scene
from core.timer import TimerSystem
from entities.player import Player
from entities.bullet import Bullet
from entities.enemy import Enemy

from entities.particle import TriangleParticle
from entities.effects import ColorParticle, FloatingText
from systems.color_system import ColorSystem
from systems.collision_system import CollisionSystem
from systems.power_bar import PowerBar
from systems.scoring_system import ScoringSystem
from misc.color_text import ColorText
from misc.aim_bar import AimBar

class GameplayScene(Scene):
    def __init__(self, game):
        self.game = game
        self.player = Player("Goat", 1)
        self.color_system = ColorSystem()
        # Load background if available
        try:
            self.background = pygame.image.load("./assets/background.png").convert()
        except Exception:
            self.background = None
        current_color = self.color_system.current_color()
        self.color_texts = [ColorText(i, current_color) for i in range(4)]
        self.collision_system = CollisionSystem()
        self.bullets = []
        self.player_bullets = []
        self.power = 1
        self.player_base_damage = 1
        # let timer system know base damage estimate
        self.player.base_damage = self.player_base_damage
        self.power_bar = PowerBar()
        self.scoring_system = ScoringSystem()
        self.timer_system = TimerSystem(self.player, self.color_system)
        self.enemy = []
        self.particles = []
        self.color_particles = []
        self.floating_texts = []
        self.player_dead = False
        if self.background:
            try:
                size = self.game.screen.get_size()
                self.background_scaled = pygame.transform.smoothscale(self.background, size)
            except Exception:
                self.background_scaled = self.background
        else:
            self.background_scaled = None
        self.aim_bar = AimBar(self.game.screen, self.player.pos)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Allow restart when dead
                if self.player_dead and event.key == pygame.K_r:
                    self.__init__(self.game)
                    return
                if event.key == pygame.K_SPACE:
                    # color switch effect
                    self.color_system.switch()
                    self.color_texts = []
                    self.power_bar.change_color(self.color_system.current_color())
                    new_color = self.color_system.current_color()
                    # spawn particles around player
                    for _ in range(20):
                        self.color_particles.append(ColorParticle(self.player.pos, new_color))
                    # floating text of color name
                    name = "Red" if new_color == self.color_system.RED else "Blue"
                    # offset text slightly to the right of player
                    self.floating_texts.append(FloatingText(self.player.pos + pygame.Vector2(20,0), name, new_color))
                    self.aim_bar.set_color(new_color)

    def update(self, delta_time):
        if self.player_dead:
            return
        # if time has expired, stop further gameplay updates
        if self.timer_system.is_time_up():
            return
        self.player.color = self.color_system.current_color()
        self.player.update(delta_time)
        if not self.color_texts:
            current_color = self.color_system.current_color()
            self.color_texts = [ColorText(i, current_color) for i in range(4)]
        for text in self.color_texts:
            text.update(delta_time) 
        for bullet in self.bullets:
            bullet.update(delta_time)
            if not self.collision_system.circle_hit(self.player, bullet):
                continue
            elif self.player.color == bullet.color:
                self.power_bar.add_power()
            else:
                self.player.health -= 25
                if self.player.health <= 0:
                    self.player_dead = True
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        for bullet in self.player_bullets:
            bullet.update(delta_time)
            for enemy in self.enemy:
                if self.collision_system.circle_hit(enemy, bullet):
                    # Increase extend time bonus for opposite color hits
                    time_bonus = 0.4 if enemy.color != self.player.color else 0.15
                    self.scoring_system.extend_time(time_bonus)
                    dead_enemy, bullets = enemy.take_damage(self.player_base_damage * self.power_bar.get_power_multiplier(), self.player.color)
                    if dead_enemy:
                        self.enemy.remove(dead_enemy)
                        self.bullets.extend(bullets)
                        for _ in range(random.randint(5, 10)):
                            self.particles.append(TriangleParticle(dead_enemy.pos, dead_enemy.color))
                        self.scoring_system.add_kill(base_score=100, enemy_hp=dead_enemy.max_health)
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
            
        

        # update particles
        for p in self.particles[:]:
            p.update(delta_time)
            if p.lifetime <= 0:
                self.particles.remove(p)
        # update color switch particles
        for p in self.color_particles[:]:
            p.update(delta_time)
            if p.lifetime <= 0:
                self.color_particles.remove(p)
        # update floating texts
        for ft in self.floating_texts[:]:
            ft.update(delta_time)
            if ft.lifetime <= 0:
                self.floating_texts.remove(ft)
        self.aim_bar.update(self.player.pos)
        
        self.power_bar.Update(delta_time)
        self.scoring_system.update(delta_time)
        for enemy in self.enemy:
            # track color change for chameleons
            prev_color = getattr(enemy, 'prev_color', enemy.color)
            enemy.update(delta_time)
            # if color changed spawn effects
            if enemy.color != prev_color:
                for _ in range(10):
                    self.color_particles.append(ColorParticle(enemy.pos, enemy.color))
                cname = "Red" if enemy.color == self.color_system.RED else "Blue"
                self.floating_texts.append(FloatingText(enemy.pos, cname, enemy.color))
            enemy.prev_color = enemy.color
            new_bullets = enemy.get_bullets()
            self.bullets.extend(new_bullets)
            # Check enemy collision with player
            if not self.player_dead and self.collision_system.circle_hit(self.player, enemy):
                self.player.health -= 50
                try:
                    self.enemy.remove(enemy)
                except ValueError:
                    pass
                if self.player.health <= 0:
                    self.player_dead = True
        self.player_bullets.extend(self.player.get_bullets())
        
        # Update timer system and get enemies to spawn
        self.timer_system.update(delta_time, self.enemy)
        self.enemy = self.timer_system.get_enemies()

        # No boss anymore; completion is handled in render when time runs out

    def render(self, screen, delta_time):   
        # Draw background if available, otherwise fill
        if self.background_scaled:
            screen.blit(self.background_scaled, (0, 0))
        else:
            screen.fill((228, 228, 228))

        # If player is dead, show death screen and stop rendering gameplay
        if self.player_dead:
            # Darken background
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            death_font = pygame.font.Font(None, 120)
            death_text = death_font.render("YOU DIED", True, (200, 0, 0))
            death_rect = death_text.get_rect(center=(screen.get_width()//2, 200))
            screen.blit(death_text, death_rect)

            score_font = pygame.font.Font(None, 48)
            score_text = score_font.render(f"FINAL SCORE: {self.scoring_system.get_score()}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(screen.get_width()//2, 320))
            screen.blit(score_text, score_rect)

            hint_font = pygame.font.Font(None, 28)
            hint = hint_font.render("Press R to restart", True, (255, 255, 255))
            hint_rect = hint.get_rect(center=(screen.get_width()//2, 380))
            screen.blit(hint, hint_rect)

            return
        for bullet in self.player_bullets:
            bullet.render(screen)
        self.player.render(screen)
        for bullet in self.bullets:
            bullet.render(screen)
        for text in self.color_texts:
            text.render(screen)
        for enemy in self.enemy:
            enemy.render(screen)
        # render particles
        for p in self.particles:
            p.render(screen)
        # render color switch particles
        for p in self.color_particles:
            p.render(screen)
        # render floating texts
        for ft in self.floating_texts:
            ft.render(screen)
        
        self.aim_bar.render()
        
        fps_font = pygame.font.Font(None, 36)
        fps_text = fps_font.render(f"FPS: {int(self.game.clock.get_fps())}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 10))
        # draw level indicator above bar
        level = int(self.timer_system.elapsed_time // 30) + 1
        lvl_font = pygame.font.Font(None, 24)
        lvl_text = lvl_font.render(f"Level {level}", True, (0,0,0))
        screen.blit(lvl_text, (100, 750 - 30))
        self.power_bar.render(screen, pygame.Vector2(100, 750),pygame.Vector2(1000, 25))
        
        # Display timer at the top
        remaining_time = self.timer_system.get_remaining_time()
        timer_text_content = self.timer_system.format_time(remaining_time)
        
        if remaining_time > 30:
            timer_color = (0, 0, 0)  # Black
        elif remaining_time > 10:
            timer_color = (200, 100, 0)  # Orange
        else:
            timer_color = (200, 0, 0)  # Red
        
        timer_font = pygame.font.Font(None, 64)
        timer_text = timer_font.render(timer_text_content, True, timer_color)
        timer_rect = timer_text.get_rect(center=(600, 30))
        screen.blit(timer_text, timer_rect)
        
        # When time is up, show results directly
        if self.timer_system.is_time_up():
            # End game results screen
            screen.fill((0, 0, 0))
            
            # Time-up message
            victory_font = pygame.font.Font(None, 100)
            victory_text = victory_font.render("TIME'S UP!", True, (0, 255, 0))
            victory_rect = victory_text.get_rect(center=(600, 150))
            screen.blit(victory_text, victory_rect)
            
            # Final score
            score_font = pygame.font.Font(None, 60)
            final_score = self.scoring_system.get_score()
            score_text = score_font.render(f"FINAL SCORE: {final_score}", True, (255, 255, 0))
            score_rect = score_text.get_rect(center=(600, 300))
            screen.blit(score_text, score_rect)
            
            # Final rank
            final_rank = self.scoring_system.get_current_rank()
            rank_font = pygame.font.Font(None, 80)
            display_rank = final_rank if final_rank else "C"
            rank_text = rank_font.render(display_rank, True, (255, 100, 0))
            rank_rect = rank_text.get_rect(center=(600, 450))
            screen.blit(rank_text, rank_rect)
            
            # Completion message
            complete_font = pygame.font.Font(None, 40)
            complete_text = complete_font.render("SUCCESS!", True, (0, 200, 255))
            complete_rect = complete_text.get_rect(center=(600, 600))
            screen.blit(complete_text, complete_rect)
            
            return
        
        # Display score on right side
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"SCORE: {self.scoring_system.get_score()}", True, (0, 0, 0))
        screen.blit(score_text, (1000, 60))
        
        # Display multiplier info on right
        streak = self.scoring_system.get_kill_streak()
        if streak > 0:
            multiplier = self.scoring_system.get_multiplier()
            
            # Display multiplier name
            name = self.scoring_system.get_multiplier_message()
            name_font = pygame.font.Font(None, 36)
            name_text = name_font.render(name, True, self.color_system.current_color())
            screen.blit(name_text, (1000, 120))
            
            # Display multiplier value underneath name
            mult_font = pygame.font.Font(None, 32)
            mult_text = mult_font.render(f"x{multiplier:.0f}", True, self.color_system.current_color())
            screen.blit(mult_text, (1000, 160))
            
            # combined multiplier/timeout bar (colored) based on remaining time
            timeout_duration = self.scoring_system.get_streak_timeout()
            time_remaining = timeout_duration - self.scoring_system.get_time_since_last_kill()
            fill_percent = max(0, time_remaining / timeout_duration)
            bar_width = 200
            bar_height = 20
            bar_x = 1000
            bar_y = 200
            # background
            pygame.draw.rect(screen, (150, 150, 150), (bar_x, bar_y, bar_width, bar_height))
            # colored fill
            pygame.draw.rect(screen, self.color_system.current_color(), (bar_x, bar_y, bar_width * fill_percent, bar_height))
            pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)
            # Draw time text
            time_text = f"{time_remaining:.1f}s"
            time_font = pygame.font.Font(None, 20)
            time_surface = time_font.render(time_text, True, (0, 0, 0))
            time_rect = time_surface.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
            screen.blit(time_surface, time_rect)