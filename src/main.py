import pygame
from game import Game
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("WILDCARD 🃏")
    clock = pygame.time.Clock()
    
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game.update()
        game.render()
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
