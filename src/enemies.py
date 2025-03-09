import pygame
import random
from settings import ENEMY_SPEED_RANGE, ENEMY_SIZE, NUM_ENEMIES, WINDOW_WIDTH, WINDOW_HEIGHT

class Enemy:
    def __init__(self):
        self.image = pygame.Surface(ENEMY_SIZE)
        self.image.fill((50, 200, 50))  # Verde
        self.rect = self.image.get_rect(
            topleft=(random.randint(0, WINDOW_WIDTH - ENEMY_SIZE[0]), random.randint(0, WINDOW_HEIGHT - ENEMY_SIZE[1]))
        )
        self.speed = random.randint(*ENEMY_SPEED_RANGE)

    def update(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed

    def render(self, screen):
        screen.blit(self.image, self.rect)

class EnemyManager:
    def __init__(self):
        self.enemies = [Enemy() for _ in range(NUM_ENEMIES)]

    def update(self, player):
        for enemy in self.enemies:
            enemy.update(player)

    def render(self, screen):
        for enemy in self.enemies:
            enemy.render(screen)
