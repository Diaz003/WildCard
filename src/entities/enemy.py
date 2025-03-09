import pygame
from src.settings import *
import random

class Enemy:
    def __init__(self):
        self.image = pygame.Surface((32, 32))
        self.image.fill(RED)
        self.rect = self.image.get_rect(
            center=(random.randint(0, WINDOW_WIDTH),
                    random.randint(0, WINDOW_HEIGHT))
        )
        self.speed = ENEMY_SPEED

    def update(self, player_rect):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = (dx**2 + dy**2)**0.5
        
        if distance > 0:  # Evita división por cero
            direction = pygame.math.Vector2(dx/distance, dy/distance)
            self.rect.center += direction * self.speed
            
            self.rect.center += direction * self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)