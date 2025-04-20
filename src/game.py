# src/game.py
import pygame
import time
from src.settings import *
from src.menu import Menu
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.boss import Boss
from src.combat import Combat
from src.rooms import Room
from src.options_menu import OptionsMenu
from src.tutorial import Tutorial
from src.pause_menu import PauseMenu

class Game:
    def __init__(self):
        # Inicialización de Pygame y audio
        pygame.init()
        pygame.mixer.init()
        self.fps = FPS
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("WILDCARD")
        self.clock = pygame.time.Clock()

        # Fondo y color base
        self.current_bg_color = BG_COLOR

        # Menú principal, opciones, tutorial y pausa
        self.menu = Menu()
        self.options_menu = None
        self.tutorial = None
        self.pause_menu = PauseMenu(self)  # Ahora usamos PauseMenu con opciones

        # Jugador y habitación
        self.room = Room()
        self.player = Player(self)

        # Niveles y enemigos
        self.current_level = 1
        self.max_levels = 3
        self.boss_spawned = False
        self.enemies = []
        self.reset_level()

        # Música
        pygame.mixer.music.set_volume(0.5)
        self.play_general_music()

        # Estado del juego
        self.combat = None
        self.combat_enemy = None
        self.game_state = "MENU"  # MENU, TUTORIAL, OPTIONS, PLAYING, COMBAT, PAUSE, GAME_OVER, VICTORY
        self.game_start_time = None
        self.elapsed_time = 0
        self.game_over_button_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, 500, 200, 50)

    # ---- Música ----
    def play_general_music(self):
        pygame.mixer.music.load('assets/music/Devastation and Revenge.mp3')
        pygame.mixer.music.play(-1)

    def play_boss_music(self):
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load('assets/music/Juhani Junkala - Epic Boss Battle [Seamlessly Looping].wav')
        pygame.mixer.music.play(-1)

    # ---- Bucle principal ----
    def run(self):
        while True:
            self.dt = self.clock.tick(self.fps) / 1000
            self.handle_events()
            self.update()
            self.draw()

    # ---- Eventos ----
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            # Toggle pausa con P o ESC
            if self.game_state == "PLAYING" and event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
                self.game_state = "PAUSE"
            elif self.game_state == "PAUSE" and event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
                # En pausa, el manejo de reanudar/otros botones está en PauseMenu
                pass

            # Manejo específico en pausa
            if self.game_state == "PAUSE":
                self.pause_menu.handle_event(event)
                continue

            # Eventos según estado
            if self.game_state == "MENU" and event.type == pygame.MOUSEBUTTONDOWN:
                for b in self.menu.buttons:
                    if b.rect.collidepoint(event.pos):
                        if b.action == "play":
                            self.game_state = "PLAYING"
                            self.game_start_time = time.time()
                        elif b.action == "tutorial":
                            self.game_state = "TUTORIAL"
                            self.tutorial = Tutorial(self)
                        elif b.action == "options":
                            self.game_state = "OPTIONS"
                            self.options_menu = OptionsMenu(self)
                        elif b.action == "quit":
                            pygame.quit()
                            raise SystemExit

            elif self.game_state == "TUTORIAL":
                self.tutorial.handle_event(event)

            elif self.game_state == "OPTIONS":
                self.options_menu.handle_event(event)

            elif self.game_state == "COMBAT":
                self.combat.handle_events(event)

            elif self.game_state == "GAME_OVER" and event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over_button_rect.collidepoint(event.pos):
                    self.reset_game()
                    self.game_state = "MENU"

            elif self.game_state == "VICTORY" and event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over_button_rect.collidepoint(event.pos):
                    self.reset_game()
                    self.game_state = "MENU"

    # ---- Lógica de juego ----
    def update(self):
        if self.game_state in ["PAUSE", "GAME_OVER", "VICTORY"]:
            return

        if self.game_state == "PLAYING":
            self.player.update(self.dt)
            if self.player.health <= 0:
                self.elapsed_time = time.time() - self.game_start_time
                self.game_state = "GAME_OVER"
                pygame.mixer.music.fadeout(1000)
                return

            # Spawnear jefe cuando no hay enemigos normales
            if not any(not isinstance(e, Boss) for e in self.enemies) and not self.boss_spawned:
                boss = Boss(self.room, min_distance=200)
                boss.health += (self.current_level - 1) * 50
                self.enemies.append(boss)
                self.boss_spawned = True
                self.play_boss_music()

            # Actualizar y colisionar todos los enemigos
            for e in list(self.enemies):
                e.update(self.player.rect, self.dt)
                if self.player.rect.colliderect(e.rect) and self.game_state != "COMBAT":
                    self.start_combat(e)

        elif self.game_state == "COMBAT":
            mouse_pos = pygame.mouse.get_pos()
            self.combat.update(self.dt, mouse_pos)
            if self.combat.state == "finished" and self.combat.transition_timer >= 2.0:
                if isinstance(self.combat_enemy, Boss):
                    if self.current_level >= self.max_levels:
                        self.game_state = "VICTORY"
                        pygame.mixer.music.fadeout(1000)
                    else:
                        self.current_level += 1
                        self.reset_level()
                        self.game_state = "PLAYING"
                        self.play_general_music()
                else:
                    self.enemies.remove(self.combat_enemy)
                    self.game_state = "PLAYING"
                self.combat = None
                self.boss_spawned = False

    def start_combat(self, enemy):
        self.game_state = "COMBAT"
        self.combat_enemy = enemy
        self.combat = Combat(self.player, enemy)

    # ---- Gestión de niveles ----
    def reset_level(self):
        self.room = Room()
        self.enemies = []
        for _ in range(5):
            e = Enemy(self.room)
            e.health += (self.current_level - 1) * 10
            e.speed *= 1 + (self.current_level - 1) * 0.05
            self.enemies.append(e)
        self.boss_spawned = False

    def reset_game(self):
        self.player.health = self.player.max_health
        self.current_level = 1
        self.reset_level()
        self.elapsed_time = 0
        self.game_start_time = None
        self.play_general_music()

    # ---- Dibujado ----
    def draw(self):
        if self.game_state == "MENU":
            mp = pygame.mouse.get_pos()
            for b in self.menu.buttons:
                b.check_hover(mp)
            self.menu.draw(self.screen)

        elif self.game_state == "TUTORIAL":
            self.tutorial.draw(self.screen)

        elif self.game_state == "OPTIONS":
            self.options_menu.draw(self.screen)

        elif self.game_state == "PLAYING":
            self.screen.fill(self.current_bg_color)
            self.room.draw(self.screen)
            self.player.draw(self.screen)
            for e in self.enemies:
                e.draw(self.screen)
            font = pygame.font.Font(None, 36)
            lvl = font.render(f"Nivel: {self.current_level}", True, WHITE)
            self.screen.blit(lvl, (20, 20))

        elif self.game_state == "COMBAT":
            self.combat.draw(self.screen)
            self.draw_combat_stats()

        elif self.game_state == "PAUSE":
            # Escena congelada
            self.screen.fill(self.current_bg_color)
            self.room.draw(self.screen)
            self.player.draw(self.screen)
            for e in self.enemies:
                e.draw(self.screen)
            # Overlay de pausa con opciones
            self.pause_menu.draw(self.screen)

        elif self.game_state == "GAME_OVER":
            self.draw_game_over()

        elif self.game_state == "VICTORY":
            self.draw_victory()

        pygame.display.update()

    def draw_combat_stats(self):
        pygame.draw.rect(self.screen, (0,255,0), (100, 500, self.player.health, 20))
        pygame.draw.rect(self.screen, (255,0,0), (1000, 500, self.combat_enemy.health, 20))

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))
        f1 = pygame.font.Font(None, 72)
        go = f1.render("GAME OVER", True, WHITE)
        self.screen.blit(go, (WINDOW_WIDTH//2 - go.get_width()//2, 150))
        f2 = pygame.font.Font(None, 36)
        dt = f2.render(f"Duraste: {int(self.elapsed_time)}s", True, WHITE)
        self.screen.blit(dt, (WINDOW_WIDTH//2 - dt.get_width()//2, 250))
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.game_over_button_rect)
        bt = f2.render("Volver al Menú", True, WHITE)
        self.screen.blit(bt, (self.game_over_button_rect.centerx - bt.get_width()//2,
                              self.game_over_button_rect.centery - bt.get_height()//2))

    def draw_victory(self):
        self.screen.fill((0, 0, 0))
        f1 = pygame.font.Font(None, 72)
        vt = f1.render("¡VICTORIA!", True, WHITE)
        self.screen.blit(vt, (WINDOW_WIDTH//2 - vt.get_width()//2, 150))
        f2 = pygame.font.Font(None, 36)
        dt = f2.render(f"Duraste: {int(time.time() - self.game_start_time)}s", True, WHITE)
        self.screen.blit(dt, (WINDOW_WIDTH//2 - dt.get_width()//2, 250))
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.game_over_button_rect)
        bt = f2.render("Volver al Menú", True, WHITE)
        self.screen.blit(bt, (self.game_over_button_rect.centerx - bt.get_width()//2,
                              self.game_over_button_rect.centery - bt.get_height()//2))

if __name__ == "__main__":
    Game().run()