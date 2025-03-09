import pygame

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/enemies/enemy.png")
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass  # Aquí puedes poner IA del enemigo

    def draw(self, screen):
        screen.blit(self.image, self.rect)
