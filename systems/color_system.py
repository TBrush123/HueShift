COLORS = [
    (255,84,78),      # Red
    (66,192,255),      # Blue
]

RED = (255,84,78) 
BLUE = (66,192,255) 

class ColorSystem:
    def __init__(self):
        self.index = 0
        self.RED = (255,84,78) 
        self.BLUE = (66,192,255)

    def switch(self):
        self.index = (self.index + 1) % 2
        
    def current_color(self):
        return RED if self.index % 2 == 0 else BLUE