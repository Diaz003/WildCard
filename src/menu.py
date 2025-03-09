# src/menu.py
import pygame
from src.settings import *

class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = BUTTON_COLOR
        self.hovered = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR

class Menu:
    def __init__(self):
        self.buttons = [
            Button("Jugar", WINDOW_WIDTH//2 - 100, 250, 200, 50, "play"),
            Button("Opciones", WINDOW_WIDTH//2 - 100, 350, 200, 50, "options"),
            Button("Salir", WINDOW_WIDTH//2 - 100, 450, 200, 50, "quit")
        ]

    def draw(self, screen):
        screen.fill(BG_COLOR)
        font = pygame.font.Font(None, 72)
        title = font.render("WILDCARD", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 150))
        screen.blit(title, title_rect)
        
        for button in self.buttons:
            button.draw(screen)