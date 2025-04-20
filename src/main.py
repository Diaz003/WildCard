# src/main.py

import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from src.game import Game  

def main():
    pygame.init()
    pygame.mixer.init()               
    pygame.mixer.music.set_volume(0.5)  
    game = Game()
    game.run()

if __name__ == "__main__":
    main()