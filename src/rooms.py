# src/rooms.py

import pygame
import random
import os
from src.settings import *

class Room:
    def __init__(self):
        self.tile_size = 64
        self.load_tiles()
        self.generate_room()

    def load_tiles(self):
        try:
            # Verifica rutas ABSOLUTAS para debug
            print(f"Buscando tiles en: {os.path.abspath('assets/Tiles')}")
            self.tiles = {
                'wall': pygame.image.load("assets/Tiles/wall.png").convert(),
                'floor': pygame.image.load("assets/Tiles/floor.png").convert(),
                'rock': pygame.image.load("assets/Tiles/rock.png").convert_alpha()
            }
            print("¡Texturas cargadas correctamente!")
        except Exception as e:
            print(f"Error cargando tiles: {e}")
            self.create_fallback_tiles()

    def create_fallback_tiles(self):
        """Crea tiles temporales si no se cargan los archivos"""
        self.tiles = {
            'wall': pygame.Surface((64, 64)).convert(),
            'floor': pygame.Surface((64, 64)).convert(),
            'rock': pygame.Surface((64, 64)).convert_alpha()
        }
        # Colores de fallback
        self.tiles['wall'].fill((100, 100, 100))  # Gris
        self.tiles['floor'].fill((200, 200, 200))   # Blanco roto
        self.tiles['rock'].fill((80, 80, 80))       # Gris oscuro
        print("Usando tiles temporales")

    def generate_room(self):
        self.width = WINDOW_WIDTH // self.tile_size
        self.height = WINDOW_HEIGHT // self.tile_size
        
        # Mapa básico (0 = suelo, 1 = muro, 2 = roca)
        self.layout = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Bordes
        for x in range(self.width):
            self.layout[0][x] = 1
            self.layout[-1][x] = 1
        for y in range(self.height):
            self.layout[y][0] = 1
            self.layout[y][-1] = 1
        
        # Rocas aleatorias
        for _ in range(random.randint(5, 10)):
            x, y = random.randint(1, self.width-2), random.randint(1, self.height-2)
            self.layout[y][x] = 2

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pos = (x * self.tile_size, y * self.tile_size)
                if self.layout[y][x] == 0:
                    screen.blit(self.tiles['floor'], pos)
                elif self.layout[y][x] == 1:
                    screen.blit(self.tiles['wall'], pos)
                elif self.layout[y][x] == 2:
                    screen.blit(self.tiles['rock'], pos)
