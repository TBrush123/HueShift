COLORS = [
    (255, 0, 0),      # Red
    (0, 0, 255),      # Blue
]

class ColorSystem:
    def __init__(self):
        self.index = 0

    def switch(self):
        self.index = (self.index + 1) % len(COLORS)
        
    def current_color(self):
        return COLORS[self.index]