import pygame
from src.settings import *
from src.menu import Menu  # <-- Agrega "src."
from src.entities.player import Player  # <-- Agrega "src."
from src.entities.enemy import Enemy  # <-- Agrega "src."
from src.combat import Combat

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("WILDCARD")
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.player = Player()
        self.enemies = [Enemy() for _ in range(5)]
        self.game_state = "MENU"
        self.combat = None

    def run(self):
        while True:
            self.dt = self.clock.tick(FPS) / 1000  # Convierte a segundos
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if self.game_state == "MENU" and event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.menu.buttons:
                    if button.hovered:
                        if button.action == "play":
                            self.game_state = "PLAYING"
                        elif button.action == "quit":
                            pygame.quit()
                            raise SystemExit

    def update(self):
        if self.game_state == "PLAYING":
            self.player.update(self.dt)
            self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]
    
            for enemy in self.enemies:
                enemy.update(self.player.rect, self.dt)  # <-- Pasa dt al enemigo
                if self.player.rect.colliderect(enemy.rect):
                    self.start_combat(enemy)
    
    def start_combat(self, enemy):
        self.game_state = "COMBAT"
        self.combat_enemy = enemy
        self.combat = Combat(self.player, enemy)

    def draw(self):
        if self.game_state == "MENU":
            mouse_pos = pygame.mouse.get_pos()
            for button in self.menu.buttons:
                button.check_hover(mouse_pos)
            self.menu.draw(self.screen)
        elif self.game_state == "PLAYING":
            self.screen.fill(BG_COLOR)
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
        elif self.game_state == "COMBAT":
            self.combat.draw(self.screen)
            self.draw_combat_stats()
        
        pygame.display.update()

    def draw_combat_stats(self):
        # Salud del jugador
        pygame.draw.rect(self.screen, (0,255,0), (100, 500, self.player.health, 20))

        # Salud del enemigo
        pygame.draw.rect(self.screen, (255,0,0), (1000, 500, self.combat_enemy.health, 20))

    def draw_health_bar(self):
        bar_width = 200
        bar_height = 20
        fill = (self.player.health / self.player.max_health) * bar_width
        pygame.draw.rect(self.screen, RED, (10, 10, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, fill, bar_height))

    def draw_timer(self):
        font = pygame.font.Font(None, 36)
        time_text = font.render("Tiempo: 00:00", True, WHITE)
        self.screen.blit(time_text, (WINDOW_WIDTH - 150, 10))