# src/combat.py
import pygame
import random
from src.settings import *
from src.entities.cards import Card

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.font = pygame.font.Font(None, 36)
        self.background = self.load_background()
        self.state = "player_turn"
        self.player_cards = self.generate_cards()
        self.enemy_attack_damage = 10
        self.delay_timer = 0
        self.transition_timer = 0
        self.enemy_turn_flash = 0.0

    def load_background(self):
        bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        bg.set_alpha(220)
        bg.fill((0, 0, 0))
        return bg

    def generate_cards(self):
        values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        cards = [Card(random.choice(values)) for _ in range(4)]
        cards.append(Card("Heal", suit="Heal"))
        random.shuffle(cards)
        return cards

    def handle_events(self, event):
        if self.state == "player_turn" and event.type == pygame.MOUSEBUTTONDOWN:
            for card in self.player_cards:
                if card.rect.collidepoint(event.pos):
                    card.is_selected = True
                    self.resolve_player_attack(card)
                    break

    def resolve_player_attack(self, card):
        if card.value == "Heal":
            heal = 20
            self.player.health = min(self.player.max_health, self.player.health + heal)
        else:
            if card.value.isdigit():
                dmg = int(card.value)*2
            else:
                dmg = 15
            self.enemy.health -= dmg
        self.state = "enemy_turn"
        self.delay_timer = 0
        self.enemy_turn_flash = 0.5
        self.player_cards = self.generate_cards()

    def update(self, dt, mouse_pos):
        if self.state == "player_turn":
            for card in self.player_cards:
                card.update(dt, mouse_pos)
        elif self.state == "enemy_turn":
            self.delay_timer += dt
            if self.delay_timer >= 1.0:
                self.player.health -= self.enemy_attack_damage
                if self.player.health > 0:
                    self.state = "player_turn"
                else:
                    self.state = "finished"
        if self.enemy_turn_flash > 0:
            self.enemy_turn_flash = max(0, self.enemy_turn_flash - dt)
        if self.enemy.health <= 0 and self.state != "finished":
            self.state = "finished"
            self.transition_timer = 0
        if self.state == "finished":
            self.transition_timer += dt

    def draw(self, screen):
        screen.blit(self.background, (0,0))
        if self.state == "enemy_turn":
            aviso = self.font.render("TURNO ENEMIGO...", True, WHITE)
            screen.blit(aviso, (WINDOW_WIDTH//2 - aviso.get_width()//2, 30))
            if self.enemy_turn_flash > 0:
                s = pygame.Surface(self.enemy.rect.size)
                s.set_alpha(int(self.enemy_turn_flash*255))
                s.fill((255,0,0))
                screen.blit(s, self.enemy.rect.topleft)
        if self.state == "player_turn":
            title = self.font.render("¡COMBATE! Selecciona una carta", True, WHITE)
            screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 30))
            card_w = 100
            total_w = len(self.player_cards)*card_w + (len(self.player_cards)-1)*20
            start_x = (WINDOW_WIDTH - total_w)//2
            for i, card in enumerate(self.player_cards):
                card.draw(screen, start_x + i*(card_w+20), WINDOW_HEIGHT//2 - 70)
        elif self.state == "finished":
            end_txt = self.font.render("¡COMBATE FINALIZADO!", True, WHITE)
            screen.blit(end_txt, (WINDOW_WIDTH//2 - end_txt.get_width()//2, 30))
        pygame.draw.rect(screen, (0,255,0), (100,500, self.player.health,20))
        pygame.draw.rect(screen, (255,0,0), (1000,500, self.enemy.health,20))
