# src/entities/animation.py
import os
import pygame

class Animation:
    def __init__(self, sprite_folder, frame_duration=100):
        self.frames = {}
        self.current_animation = 'idle'
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = frame_duration
        
        # Cargar todas las animaciones
        for animation_name in os.listdir(sprite_folder):
            animation_path = os.path.join(sprite_folder, animation_name)
            if os.path.isdir(animation_path):
                self.frames[animation_name] = []
                for frame_file in sorted(os.listdir(animation_path)):
                    frame_path = os.path.join(animation_path, frame_file)
                    image = pygame.image.load(frame_path).convert_alpha()
                    self.frames[animation_name].append(image)

    def update(self, animation_name):
        # Cambiar animación si es diferente
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.frame_index = 0
        
        # Avanzar frame
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.current_animation])
            self.last_update = now

    def get_current_frame(self):
        return self.frames[self.current_animation][self.frame_index]