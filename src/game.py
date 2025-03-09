import pygame
from player_module import Player
from enemies import Enemy
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.enemies = [Enemy(100, 100), Enemy(400, 200), Enemy(600, 300)]  # Lista de enemigos

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)

        # Actualizar enemigos (seguir al jugador)
        for enemy in self.enemies:
            enemy.update(self.player)

    def render(self):
        self.screen.fill((30, 30, 30))  # Fondo oscuro

        # Dibujar al jugador
        self.player.render(self.screen)

        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.render(self.screen)
