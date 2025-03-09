import pygame
from player import Player
from rooms import RoomManager
from enemies import EnemyManager

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.room_manager = RoomManager()
        self.enemy_manager = EnemyManager()

    def update(self):
        self.player.update()
        self.enemy_manager.update(self.player)

    def render(self):
        self.screen.fill((30, 30, 30))  # Fondo oscuro
        self.room_manager.render(self.screen)
        self.enemy_manager.render(self.screen)
        self.player.render(self.screen)
