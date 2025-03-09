import pygame
import random

class Room:
    def __init__(self):
        self.color = [random.randint(50, 200) for _ in range(3)]  # Color aleatorio

    def render(self, screen):
        screen.fill(self.color)

class RoomManager:
    def __init__(self):
        self.current_room = Room()

    def update(self):
        pass  # Se puede agregar lógica para cambiar de habitación

    def render(self, screen):
        self.current_room.render(screen)
