# src/combat.py
import pygame
from src.settings import *

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.cards = ["Ataque", "Defensa", "Hechizo"]  # Cartas básicas
        self.selected_card = None
        self.font = pygame.font.Font(None, 36)
        self.combat_active = True

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected_card = self.cards[0]
            elif event.key == pygame.K_2:
                self.selected_card = self.cards[1]
            elif event.key == pygame.K_3:
                self.selected_card = self.cards[2]

    def resolve_combat(self):
        if self.selected_card == "Ataque":
            self.enemy.health -= 20
        elif self.selected_card == "Defensa":
            self.player.health += 10
        elif self.selected_card == "Hechizo":
            self.enemy.health -= 15
            
        self.combat_active = False

    def draw(self, screen):
        # Fondo del combate
        pygame.draw.rect(screen, (40, 40, 40), (200, 100, 800, 400))
        
        # Texto del combate
        text = self.font.render("¡COMBATE! Elige una carta:", True, WHITE)
        screen.blit(text, (300, 150))
        
        # Cartas
        for i, card in enumerate(self.cards):
            card_rect = pygame.Rect(300 + i*200, 250, 150, 200)
            pygame.draw.rect(screen, (70, 70, 70), card_rect)
            text = self.font.render(card, True, WHITE)
            screen.blit(text, (card_rect.x + 20, card_rect.y + 20))
            text = self.font.render(f"({i+1})", True, WHITE)
            screen.blit(text, (card_rect.x + 20, card_rect.y + 170))