import pygame
import os
from src.settings import *

class Player:
    def __init__(self):
        # Configuración inicial
        self.direction = pygame.math.Vector2()
        self.status = 'idle'
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        
        # Cargar animaciones
        self.animations = {
            'idle': self.load_animation_frames('idle'),
            'walk': self.load_animation_frames('walk')
        }
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

    def load_animation_frames(self, animation_name):
        path = f"assets/characters/jack/{animation_name}"
        frames = []
        for frame in sorted(os.listdir(path)):
            frame_path = os.path.join(path, frame)
            image = pygame.image.load(frame_path).convert_alpha()  # Usar convert_alpha()
            image = pygame.transform.scale(image, (64, 64))  # Tamaño más visible
            frames.append(image)
        return frames

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            self.status = 'walk'
        else:
            self.status = 'idle'

    def update(self):
        self.handle_input()
        self.animate()
        self.rect.center += self.direction * self.speed

    def animate(self):
        # Cambiar frames según la animación
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.respawn()

    def respawn(self):
        self.health = self.max_health
        self.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
