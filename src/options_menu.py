# src/options_menu.py
import pygame
from src.settings import *
from src.menu import Button

class OptionsMenu:
    def __init__(self, game):
        self.game = game
        self.resolutions = [(1280, 720), (800, 600)]
        self.current_resolution_index = 0
        self.resolution_button = Button(
            f"Resolución: {self.resolutions[self.current_resolution_index][0]}x{self.resolutions[self.current_resolution_index][1]}",
            WINDOW_WIDTH//2 - 150, 200, 300, 50, "toggle_resolution"
        )
        self.bg_colors = {"Oscuro": (30, 30, 30), "Claro": (200, 200, 200)}
        self.bg_color_keys = list(self.bg_colors.keys())
        self.current_bg_index = 0
        self.bg_color_button = Button(
            f"Color Fondo: {self.bg_color_keys[self.current_bg_index]}",
            WINDOW_WIDTH//2 - 150, 270, 300, 50, "toggle_bg"
        )
        self.fps_options = [30, 60, 120]
        self.current_fps_index = 1 
        self.fps_button = Button(
            f"FPS: {self.fps_options[self.current_fps_index]}",
            WINDOW_WIDTH//2 - 150, 340, 300, 50, "toggle_fps"
        )
        self.back_button = Button("Volver", WINDOW_WIDTH//2 - 100, 410, 200, 50, "back")
        self.buttons = [self.resolution_button, self.bg_color_button, self.fps_button, self.back_button]

    def draw(self, screen):
        screen.fill(self.game.current_bg_color)
        font = pygame.font.Font(None, 72)
        title = font.render("Opciones", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        screen.blit(title, title_rect)
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    if button.action == "toggle_resolution":
                        self.toggle_resolution()
                    elif button.action == "toggle_bg":
                        self.toggle_bg()
                    elif button.action == "toggle_fps":
                        self.toggle_fps()
                    elif button.action == "back":
                        self.game.game_state = "MENU"

    def toggle_resolution(self):
        self.current_resolution_index = (self.current_resolution_index + 1) % len(self.resolutions)
        res = self.resolutions[self.current_resolution_index]
        self.resolution_button.text = f"Resolución: {res[0]}x{res[1]}"
        self.game.screen = pygame.display.set_mode(res)

    def toggle_bg(self):
        self.current_bg_index = (self.current_bg_index + 1) % len(self.bg_color_keys)
        key = self.bg_color_keys[self.current_bg_index]
        self.bg_color_button.text = f"Color Fondo: {key}"
        self.game.current_bg_color = self.bg_colors[key]

    def toggle_fps(self):
        self.current_fps_index = (self.current_fps_index + 1) % len(self.fps_options)
        new_fps = self.fps_options[self.current_fps_index]
        self.fps_button.text = f"FPS: {new_fps}"
        self.game.fps = new_fps
