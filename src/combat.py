import pygame
import random
from cards import Deck
from settings import Settings

class CombatHandler:
    def __init__(self, player):
        self.settings = Settings()
        self.player = player
        self.deck = Deck()
        self.enemy = None
        self.combat_over = False
        self.player_hand = []
        self.enemy_hand = []
        self.selected_cards = []
        self.timer = 30
        self.font = pygame.font.Font(None, 36)
        self.card_positions = []

    def start_combat(self, enemy):
        self.enemy = enemy
        self.combat_over = False
        self.player_hand = [self.deck.draw_card() for _ in range(5)]
        self.enemy_hand = [self.deck.draw_card() for _ in range(5)]
        self.timer = 30
        self.selected_cards = []

    def update(self):
        for card in self.player_hand + self.enemy_hand:
            card.update_animation()
        
        self.timer -= 1/60
        if self.timer <= 0 or len(self.selected_cards) == 3:
            self.resolve_combat()
        self.selected_cards = []

    def update(self):
        for card in self.player_hand + self.enemy_hand:
            card.update_animation()
        
        self.timer -= 1/60
        if self.timer <= 0 or len(self.selected_cards) == 3:
            self.resolve_combat()

    def evaluate_hand(self, hand):
        ranks = sorted([card.value for card in hand])
        suits = [card.suit for card in hand]
        
        counts = {r: ranks.count(r) for r in set(ranks)}
        unique_ranks = len(counts)
        
        straight = (max(ranks) - min(ranks) == 4) and (unique_ranks == 5)
        flush = len(set(suits)) == 1
        
        if straight and flush: return "Straight Flush", 50
        if 4 in counts.values(): return "Four of a Kind", 25
        if 3 in counts.values() and 2 in counts.values(): return "Full House", 20
        if flush: return "Flush", 15
        if straight: return "Straight", 12
        if 3 in counts.values(): return "Three of a Kind", 8
        if list(counts.values()).count(2) == 2: return "Two Pair", 5
        if 2 in counts.values(): return "Pair", 2
        return "High Card", 1

    def handle_click(self, pos):
        for card, (x, y) in zip(self.player_hand, self.card_positions):
            if card.rect.collidepoint(pos):
                card.is_selected = not card.is_selected
                if card.is_selected and len(self.selected_cards) < 3:
                    self.selected_cards.append(card)
                else:
                    self.selected_cards.remove(card)

    def resolve_combat(self):
        if len(self.selected_cards) != 3:
            self.player.health -= 10
            return  # Termina aquí si el jugador no elige 3 cartas
        
        player_power = self.evaluate_hand(self.selected_cards)[1]
        enemy_power = self.evaluate_hand(random.sample(self.enemy_hand, 3))[1]
    
        if player_power > enemy_power:
            self.enemy.take_damage(player_power * 10)
        else:
            self.player.health -= enemy_power * 10
    
        # Mover cartas usadas al descarte
        self.deck.discard_pile.extend(self.selected_cards + self.enemy_hand)
        self.combat_over = True

    def update(self):
        # Actualizar animaciones
        for card in self.player_hand + self.enemy_hand:
            card.update_animation()
        
        self.timer -= 1/60
        if self.timer <= 0 or len(self.selected_cards) == 3:
            self.resolve_combat()

    def draw(self, screen):
        screen.fill((30, 30, 30))
        self.draw_hand(screen, self.player_hand, self.settings.HEIGHT - 200)  # <-- Llamada al método
        
        # Cartas enemigas
        if self.player_hand:
            card_width = self.player_hand[0].rect.width
            for i, _ in enumerate(self.enemy_hand):
                x = 100 + i * (card_width + 20)
                y = 50
                pygame.draw.rect(screen, (200, 50, 50), (x, y, card_width, 178))  # 178 = altura carta
        
        # Temporizador
        timer_text = self.font.render(f"Tiempo: {int(self.timer)}", True, (255, 255, 255))
        screen.blit(timer_text, (20, 20))

    # ¡Método añadido!
    def draw_hand(self, screen, hand, y_pos):
        if not hand:
            return
            
        card_width = hand[0].rect.width
        spacing = 20
        start_x = (self.settings.WIDTH - (len(hand) * (card_width + spacing))) // 2
        
        self.card_positions = []
        for i, card in enumerate(hand):
            x = start_x + i * (card_width + spacing)
            card.draw(screen, (x, y_pos))
            self.card_positions.append((x, y_pos))