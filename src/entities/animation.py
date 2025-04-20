# src/entities/animation.py

import pygame
import os

class Animation:
    def __init__(self, sprite_folder, frame_duration=0.1):
        self.frames = self.load_frames(sprite_folder)
        self.frame_index = 0
        self.frame_duration = frame_duration
        self.timer = 0.0

    def load_frames(self, folder_path):
        try:
            files = sorted(
                [f for f in os.listdir(folder_path) if f.endswith('.png')],
                key=lambda x: int(x.split('_')[-1].split('.')[0])
            )
            return [pygame.image.load(os.path.join(folder_path, f)).convert_alpha() for f in files]
        except FileNotFoundError:
            print(f"Error: Carpeta {folder_path} no encontrada")
            return [pygame.Surface((100, 140))]
        except Exception as e:
            print(f"Error cargando animación: {e}")
            return [pygame.Surface((100, 140))]

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.frame_index]

    @classmethod
    def from_surface(cls, surface, frame_duration=0.1):
        instance = cls(sprite_folder="", frame_duration=frame_duration)
        instance.frames = [surface]
        instance.frame_index = 0
        instance.timer = 0.0
        return instance
