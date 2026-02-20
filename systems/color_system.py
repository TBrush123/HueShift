COLORS = [
    (255,84,78),      # Red
    (66,192,255),      # Blue
]

class ColorSystem:
    def __init__(self):
        self.index = 0

    def switch(self):
        self.index = (self.index + 1) % len(COLORS)
        
    def current_color(self):
        return COLORS[self.index]