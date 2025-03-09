import pygame

class UI:
    def __init__(self, font_size=30):
        self.font = pygame.font.Font(None, font_size)

    def render_text(self, screen, text, x, y, color=(255, 255, 255)):
        surface = self.font.render(text, True, color)
        screen.blit(surface, (x, y))
