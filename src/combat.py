# src/combat.py
import pygame
import random
from src.settings import *
from src.entities.cards import Card

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.cards = self.generate_cards()
        self.font = pygame.font.Font(None, 36)
        self.background = self.load_background()

    def generate_cards(self):  # <-- Método dentro de la clase
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        return [Card(random.choice(values)) for _ in range(5)]

    def load_background(self):
        bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        bg.set_alpha(200)
        bg.fill((0, 0, 0))
        return bg

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in self.cards:
                if card.rect.collidepoint(event.pos):
                    self.resolve_combat(card)

    def resolve_combat(self, card):
        if card.value.isdigit():
            damage = int(card.value) * 2
        else:
            damage = 15
        
        self.enemy.health -= damage
        self.player.take_damage(5)

    def update(self, dt, mouse_pos):
        for card in self.cards:
            card.update(dt, mouse_pos)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        text = self.font.render("¡COMBATE! Selecciona una carta", True, WHITE)
        screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 50))
        
        for i, card in enumerate(self.cards):
            card.draw(screen, 200 + i*250, WINDOW_HEIGHT//2 - 70)