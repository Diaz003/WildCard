# src/tutorial.py

import pygame
from src.settings import *

class Tutorial:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.instructions = [
            "Bienvenido al Tutorial de WILDCARD",
            "",
            "COMBATE:",
            "  - En combate, el turno es por fases.",
            "  - En tu turno, selecciona una carta de ataque para dañar al enemigo",
            "    o la carta 'Heal' para curarte.",
            "  - La carta de curación te restaura 20 puntos de vida.",
            "  - Luego, el enemigo ataca.",
            "",
            "CONTROLES:",
            "  - Usa WASD para moverte.",
            "  - Usa el ratón para interactuar en los menús y en combate.",
            "",
            "Presiona cualquier tecla o haz clic para volver al menú."
        ]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.game.game_state = "MENU"

    def draw(self, screen):
        screen.fill(BG_COLOR)
        y_offset = 50
        for line in self.instructions:
            text = self.font.render(line, True, WHITE)
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, y_offset))
            y_offset += 40
