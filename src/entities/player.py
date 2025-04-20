# src/entities/player.py

import pygame
from src.settings import *
from src.entities.animation import Animation

class Player:
    def __init__(self, game):
        self.game = game
        self.direction = pygame.math.Vector2()
        self.status = "idle"
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.animations = {
            "idle": Animation("assets/Characters/jack/idle"),
            "walk": Animation("assets/Characters/jack/walk")
        }
        self.current_animation = self.animations["idle"]
        self.image = self.current_animation.get_current_frame()
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            self.status = "walk"
        else:
            self.status = "idle"

    def animate(self, dt):
        self.current_animation = self.animations[self.status]
        self.current_animation.update(dt)
        self.image = self.current_animation.get_current_frame()

    def update(self, dt):
        old_pos = self.rect.copy()
        self.handle_input()
        self.rect.center += self.direction * self.speed * dt
        self.animate(dt)
        for y in range(self.game.room.height):
            for x in range(self.game.room.width):
                if self.game.room.layout[y][x] in [1, 2]:
                    tile_rect = pygame.Rect(
                        x * self.game.room.tile_size,
                        y * self.game.room.tile_size,
                        self.game.room.tile_size,
                        self.game.room.tile_size
                    )
                    if self.rect.colliderect(tile_rect):
                        self.rect = old_pos
                        break

    def draw(self, screen):
        screen.blit(self.image, self.rect)
