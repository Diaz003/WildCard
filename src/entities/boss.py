# src/entities/boss.py
import pygame
from src.settings import *
from src.entities.enemy import Enemy

class Boss(Enemy):
    def __init__(self, room, min_distance=200):
        super().__init__(room, min_distance)
        # Salud y velocidad propias del jefe
        self.max_health = 200
        self.health = self.max_health
        self.speed = ENEMY_SPEED * 0.5
        # Sprite distinto (más grande y púrpura)
        self.image = pygame.Surface((64, 64))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, player_rect, dt):
        # Movimiento igual al de Enemy pero con dt
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = (dx**2 + dy**2)**0.5
        if dist > 0 and dist < 600:  # rango de detección más amplio
            direction = pygame.math.Vector2(dx/dist, dy/dist)
            self.rect.center += direction * self.speed * dt
