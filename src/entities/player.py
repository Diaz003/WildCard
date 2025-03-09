# src/entities/player.py
import pygame
from src.settings import *
from src.entities.animation import Animation  # Importa la clase Animation

class Player:
    def __init__(self):
        self.direction = pygame.math.Vector2()
        self.status = "idle"
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        
        # Carga las animaciones
        self.animations = {
            "idle": Animation("assets/characters/jack/idle"),
            "walk": Animation("assets/characters/jack/walk")
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

    def update(self, dt):
        self.handle_input()
        self.animate(dt)  # <-- Llama al método animate
        self.rect.center += self.direction * self.speed * dt

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def animate(self, dt):
        # Actualiza la animación según el estado
        self.current_animation = self.animations[self.status]
        self.current_animation.update(dt)
        self.image = self.current_animation.get_current_frame()