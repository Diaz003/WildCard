# game/jack.py
import pygame
import os

class Jack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_animations()
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_speed = 100  # ms entre frames
        self.last_update = pygame.time.get_ticks()
        
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.direction = "right"
        
        # Atributos de juego
        self.health = 100
        self.max_health = 100
        self.card_power = 1.0

    def load_animations(self):
        self.animations = {
            "idle": self.load_frames("idle", 4),
            "walk": self.load_frames("walk", 6),
            "hurt": self.load_frames("hurt", 3),
            "attack": self.load_frames("attack", 5)
        }

    def load_frames(self, action, frame_count):
        frames = []
        base_path = os.path.join("assets", "characters", "jack", action)
        
        try:
            for i in range(frame_count):
                frame_path = os.path.join(base_path, f"jack_{action}_{i:02}.png")
                img = pygame.image.load(frame_path).convert_alpha()
                frames.append(pygame.transform.scale_by(img, 2))  # Escala 2x
        except FileNotFoundError:
            # Fallback: crear frames básicos
            frames = [self.create_debug_frame(action)]
            
        return frames

    def create_debug_frame(self, action):
        temp_surface = pygame.Surface((32, 48))
        color = (40, 40, 40) if action == "idle" else (120, 30, 30)
        temp_surface.fill(color)
        return temp_surface

    def update(self, keys):
        now = pygame.time.get_ticks()
        
        # Animación
        if now - self.last_update > self.animation_speed:
            self.animation_frame = (self.animation_frame + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.animation_frame]
            self.last_update = now
            
            if self.direction == "left":
                self.image = pygame.transform.flip(self.image, True, False)
        
        # Movimiento
        dx, dy = 0, 0
        if keys[pygame.K_a]: dx -= self.speed
        if keys[pygame.K_d]: dx += self.speed
        if keys[pygame.K_w]: dy -= self.speed
        if keys[pygame.K_s]: dy += self.speed
        
        if dx != 0 or dy != 0:
            self.current_animation = "walk"
            self.direction = "right" if dx > 0 else "left" if dx < 0 else self.direction
        else:
            self.current_animation = "idle"
            
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        # Sombras
        shadow = pygame.Surface((self.rect.width//2, 10))
        shadow.set_alpha(100)
        screen.blit(shadow, (self.rect.centerx - shadow.get_width()//2, self.rect.bottom - 5))
        
        # Dibujar personaje
        screen.blit(self.image, self.rect)
        
        # Barra de salud
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 6
        pos = (self.rect.centerx - bar_width//2, self.rect.top - 15)
        
        # Fondo
        pygame.draw.rect(screen, (40, 40, 40), (*pos, bar_width, bar_height))
        # Salud actual
        pygame.draw.rect(screen, (200, 30, 30), 
                        (pos[0], pos[1], bar_width * (self.health/self.max_health), bar_height))