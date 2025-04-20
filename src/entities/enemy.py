# src/entities/enemy.py

import pygame
import random
from src.settings import *

class Enemy:
    def __init__(self, room, min_distance=200):
        self.image = pygame.Surface((32, 32))
        self.image.fill(RED)
        valid_position = False
        while not valid_position:
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(50, WINDOW_HEIGHT - 50)
            if ((x - WINDOW_WIDTH//2)**2 + (y - WINDOW_HEIGHT//2)**2)**0.5 > min_distance:
                valid_position = True
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = ENEMY_SPEED
        self.health = 50
        self.room = room

    def update(self, player_rect, dt):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = (dx**2 + dy**2)**0.5
        if distance > 0 and distance < 500:
            direction = pygame.math.Vector2(dx/distance, dy/distance)
            self.rect.center += direction * self.speed * dt

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    