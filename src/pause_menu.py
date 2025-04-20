# src/pause_menu.py
import pygame
from src.settings import *
from src.menu import Button

class PauseMenu:
    def __init__(self, game):
        self.game = game
        # Configura botones: Reanudar, Opciones, Volver al Menú
        center_x = WINDOW_WIDTH // 2
        base_y = WINDOW_HEIGHT // 2 - 50
        spacing = 70
        self.buttons = [
            Button("Reanudar", center_x - 100, base_y, 200, 50, action="resume"),
            Button("Opciones", center_x - 100, base_y + spacing, 200, 50, action="options"),
            Button("Menú Principal", center_x - 100, base_y + 2*spacing, 200, 50, action="menu")
        ]
        # Overlay semitransparente
        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.overlay.set_alpha(150)
        self.overlay.fill((0, 0, 0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                if btn.rect.collidepoint(pos):
                    if btn.action == "resume":
                        self.game.game_state = "PLAYING"
                    elif btn.action == "options":
                        self.game.game_state = "OPTIONS"
                        self.game.options_menu = OptionsMenu(self.game)
                    elif btn.action == "menu":
                        # Reset game and return to menu
                        self.game.reset_game()
                        self.game.game_state = "MENU"
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            for btn in self.buttons:
                btn.check_hover(pos)

    def draw(self, screen):
        # Dibuja overlay
        screen.blit(self.overlay, (0, 0))
        # Dibuja cada botón
        for btn in self.buttons:
            btn.draw(screen)

# Nota: Asegúrate de importar OptionsMenu en la parte superior si no está ya importado:
from src.options_menu import OptionsMenu
