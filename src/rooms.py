import pygame

class Room:
    def __init__(self):
        self.image = pygame.image.load("assets/rooms/room1.png")
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
