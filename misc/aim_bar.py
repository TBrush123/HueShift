import pygame
import systems.color_system

class AimBar:
    def __init__(self, screen: pygame.Surface, player_pos: list | tuple,
                 dash_len: int = 18, gap_len: int = 8, thickness: int = 2,
                 cross_x: int = 20, cross_size: int = 8):
        self.screen = screen
        self.player_pos = player_pos
        self.dash_len = dash_len
        self.gap_len = gap_len
        self.thickness = thickness
        self.cross_x = cross_x
        self.cross_size = cross_size

        #Initial color 
        self._set_colors(systems.color_system.RED)

    def set_color(self, color):
        """Change the bar color. Pass only the base RGB color — transparent variant is auto-generated."""
        self._set_colors(color)

    def _set_colors(self, color):
        self.color = color
        self.color_transparent = (*color[:3], 80)  # same color, low alpha

    def update(self, player_pos: list | tuple):
        """Update the aim bar's tracked position (call each frame with current player pos)."""
        self.player_pos = player_pos

    def render(self):
        """Draw the dashed aim line and crosshair onto the screen."""
        px, py = int(self.player_pos[0]), int(self.player_pos[1])
        mx, my = pygame.mouse.get_pos()
        screen_w, screen_h = self.screen.get_size()

        dx = mx - px
        dy = my - py
        length = (dx ** 2 + dy ** 2) ** 0.5

        if length == 0:
            return

        # Normalized direction
        nx, ny = dx / length, dy / length

        # Find the farthest t to reach any screen edge in the aim direction
        ts = []
        if nx != 0:
            ts.append((0 - px) / nx)
            ts.append((screen_w - px) / nx)
        if ny != 0:
            ts.append((0 - py) / ny)
            ts.append((screen_h - py) / ny)

        max_t = max((t for t in ts if t > 0), default=length)

        # --- Dashed line from player to screen edge ---
        line_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

        current_t = 0
        drawing = True
        while current_t < max_t:
            seg = self.dash_len if drawing else self.gap_len
            end_t = min(current_t + seg, max_t)
            if drawing:
                x1 = int(px + nx * current_t)
                y1 = int(py + ny * current_t)
                x2 = int(px + nx * end_t)
                y2 = int(py + ny * end_t)
                pygame.draw.line(line_surface, self.color_transparent, (x1, y1), (x2, y2), self.thickness)
            current_t += seg
            drawing = not drawing

        self.screen.blit(line_surface, (0, 0))

        # --- Thick crosshair at mouse position ---
        cs = self.cross_size
        cross_thickness = max(2, self.thickness + 1)
        pygame.draw.line(self.screen, self.color, (mx - cs, my), (mx + cs, my), cross_thickness)
        pygame.draw.line(self.screen, self.color, (mx, my - cs), (mx, my + cs), cross_thickness)