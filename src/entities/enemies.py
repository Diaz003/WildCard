import pygame
import random
from src.settings import *

class Enemy:
    def __init__(self):
        self.image = pygame.Surface((32, 32))  # Sprite temporal (cambia por tus imágenes)
        self.image.fill(RED)
        self.rect = self.image.get_rect(
            center=(random.randint(50, WINDOW_WIDTH-50),
                    random.randint(50, WINDOW_HEIGHT-50))
        )
        self.speed = ENEMY_SPEED
        self.health = 50

    def update(self, player_rect):
        # Movimiento hacia el jugador
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = (dx**2 + dy**2)**0.5

        if distance > 0 and distance < 500:  # Rango de detección
            direction = pygame.math.Vector2(dx/distance, dy/distance)
            self.rect.center += direction * self.speed

    def draw(self, screen):  # <-- ¡Este método faltaba!
        screen.blit(self.image, self.rect)

    def kill(self):  # Opcional: Para eliminar enemigos derrotados
        self.health = 0