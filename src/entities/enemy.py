# entities/enemy.py
import pygame
import random
from src.settings import *

class Enemy:
    def __init__(self):
        self.image = pygame.Surface((32, 32))
        self.image.fill(RED)
        self.rect = self.image.get_rect(
            center=(random.randint(50, WINDOW_WIDTH-50),
                    random.randint(50, WINDOW_HEIGHT-50))
        )
        self.speed = ENEMY_SPEED
        self.health = 50

    def update(self, player_rect, dt):  # <-- Añade dt como parámetro
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = (dx**2 + dy**2)**0.5
    
        if distance > 0 and distance < 500:
            direction = pygame.math.Vector2(dx/distance, dy/distance)
            self.rect.center += direction * self.speed * dt  # <-- Usa dt aquí

    # AÑADE ESTE MÉTODO
    def draw(self, screen):
        screen.blit(self.image, self.rect)