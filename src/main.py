import pygame
from src.game import Game
from .settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS 

def main():
    pygame.init()
    game = Game()
    game.run()

if __name__ == "__main__":
    main()