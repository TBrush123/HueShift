import pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((228, 228, 228))
    pygame.draw.circle(screen, (100, 0, 0), (600, 400), 20)
    
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)