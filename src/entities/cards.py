# src/entities/cards.py

import pygame
import os
from src.settings import *
from src.entities.animation import Animation

class Card:
    def __init__(self, value, suit="Corazón"):
        self.value = value
        self.suit = suit
        self.animation = self.load_animation()
        self.rect = pygame.Rect(0, 0, 100, 140)
        self.is_selected = False
        self.hovered = False
        self.scale_factor = 1.0

    def load_animation(self):
        try:
            if self.value == "Heal":
                surf = pygame.Surface((100, 140))
                surf.fill((0, 255, 0))  # Verde brillante para curación
                return Animation.from_surface(surf)
            path = os.path.join("assets", "Cartas", "PNG", self.suit, self.value)
            print(f"Intentando cargar animación desde: {path}")
            if not os.path.exists(path):
                raise FileNotFoundError
            return Animation(path, frame_duration=0.1)
        except Exception as e:
            print(f"Error cargando carta {self.value}: {str(e)}")
            surf = pygame.Surface((100, 140))
            surf.fill((50, 50, 200))
            return Animation.from_surface(surf)

    def update(self, dt, mouse_pos):
        self.animation.update(dt)
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and self.scale_factor < 1.1:
            self.scale_factor += dt * 2
        elif not self.hovered and self.scale_factor > 1.0:
            self.scale_factor -= dt * 2

    def draw(self, screen, x, y):
        frame = self.animation.get_current_frame()
        scaled_width = int(100 * self.scale_factor)
        scaled_height = int(140 * self.scale_factor)
        scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
        pos_x = x - (scaled_width - 100) // 2
        pos_y = y - (scaled_height - 140) // 2
        self.rect = pygame.Rect(pos_x, pos_y, scaled_width, scaled_height)
        screen.blit(scaled_frame, (pos_x, pos_y))
        if self.is_selected:
            pygame.draw.rect(screen, (255, 215, 0), (pos_x-5, pos_y-5, scaled_width+10, scaled_height+10), 3)
