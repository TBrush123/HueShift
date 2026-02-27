import pygame

from core.scene import Scene
from scenes.gameplay import GameplayScene


class MainMenuScene(Scene):
    def __init__(self, game):
        self.game = game
        # optionally preload fonts or images here
        try:
            self.title_font = pygame.font.Font(None, 80)
            self.inst_font = pygame.font.Font(None, 36)
        except Exception:
            self.title_font = pygame.font.SysFont("arial", 80)
            self.inst_font = pygame.font.SysFont("arial", 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # start the game on Enter or Space
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.game.scene = GameplayScene(self.game)
                # allow quitting from menu
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

    def update(self, delta):
        # nothing to update on static menu
        pass

    def render(self, screen, delta):
        # simple dark background
        screen.fill((20, 20, 20))

        # title
        title_surf = self.title_font.render("HUE SHIFT", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title_surf, title_rect)

        # instructions
        instructions = [
            "WASD to move",
            "Left click to shoot",
            "Space to switch color",
            "Survive for 4 minutes and rack up points",
            "Press ENTER or SPACE to start",
            "Esc to quit"
        ]
        for i, line in enumerate(instructions):
            text = self.inst_font.render(line, True, (200, 200, 200))
            rect = text.get_rect(center=(screen.get_width() // 2, 250 + i * 50))
            screen.blit(text, rect)
