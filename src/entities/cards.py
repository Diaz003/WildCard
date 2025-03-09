# entities/cards.py
import pygame
from src.settings import *
from src.entities.animation import Animation  # Importa la clase Animation
import os

class Card:
    def __init__(self, value, suit="Corazón"):
        self.value = value
        self.suit = suit
        self.animation = self.load_animation()
        self.rect = pygame.Rect(0, 0, 100, 140)
        self.is_selected = False
        self.hovered = False

    def load_animation(self):
        path = os.path.join("assets", "Cartas", "PNG", self.suit, self.value)
        return Animation(path, frame_duration=0.08)  # Animación más rápida

    def update(self, dt, mouse_pos):
        self.animation.update(dt)
        self.hovered = self.rect.collidepoint(mouse_pos)  # Detección de hover

    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        frame = pygame.transform.scale(self.animation.get_current_frame(), (110, 154))  # Efecto hover
        screen.blit(frame, (x-5 if self.hovered else x, y-5 if self.hovered else y))
        
        # Resaltados
        if self.is_selected:
            pygame.draw.rect(screen, (255, 215, 0), (x-5, y-5, 120, 154), 3)
        elif self.hovered:
            pygame.draw.rect(screen, (200, 200, 200), (x-5, y-5, 120, 154), 3)