import pygame
import random
import sys
import math
import json
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Inicializar pygame
pygame.init()

# Configurações da tela
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Cores modernas
class Colors:
    BACKGROUND = (15, 15, 25)
    GRID_LINE = (25, 25, 40)
    SNAKE_HEAD = (100, 255, 100)
    SNAKE_BODY = (50, 200, 50)
    SNAKE_TAIL = (30, 150, 30)
    FOOD_NORMAL = (255, 100, 100)
    FOOD_SPECIAL = (255, 215, 0)
    FOOD_BONUS = (255, 20, 147)
    TEXT_PRIMARY = (255, 255, 255)
    TEXT_SECONDARY = (180, 180, 180)
    UI_BACKGROUND = (20, 20, 35)
    UI_BORDER = (60, 60, 80)
    NEON_GREEN = (57, 255, 20)
    NEON_BLUE = (20, 100, 255)
    NEON_PINK = (255, 20, 147)
    PARTICLE_COLORS = [(255, 100, 100), (255, 150, 50), (255, 200, 0), (255, 255, 100)]

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

@dataclass
class Position:
    x: int
    y: int
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Particle:
    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.color = color
        self.size = random.uniform(2, 6)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
        self.life -= 1
        return self.life > 0
    
    def draw(self, surface: pygame.Surface):
        alpha = int(255 * (self.life / self.max_life))
        size = int(self.size * (self.life / self.max_life))
        if size > 0:
            color = (*self.color, alpha)
            # Criar superfície temporária para alpha blending
            temp_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, color, (size, size), size)
            surface.blit(temp_surface, (self.x - size, self.y - size))

class Food:
    def __init__(self, position: Position, food_type: str = "normal"):
        self.position = position
        self.type = food_type
        self.animation_offset = 0
        self.pulse_speed = 0.1
        self.spawn_time = pygame.time.get_ticks()
        
        # Propriedades baseadas no tipo
        if food_type == "normal":
            self.color = Colors.FOOD_NORMAL
            self.points = 10
            self.lifetime = None
        elif food_type == "special":
            self.color = Colors.FOOD_SPECIAL
            self.points = 25
            self.lifetime = 10000  # 10 segundos
        elif food_type == "bonus":
            self.color = Colors.FOOD_BONUS
            self.points = 50
            self.lifetime = 5000   # 5 segundos
    
    def update(self):
        self.animation_offset += self.pulse_speed
        
        # Verificar se expirou
        if self.lifetime:
            elapsed = pygame.time.get_ticks() - self.spawn_time
            return elapsed < self.lifetime
        return True
    
    def draw(self, surface: pygame.Surface):
        # Calcular posição na tela
        screen_x = self.position.x * GRID_SIZE
        screen_y = self.position.y * GRID_SIZE
        
        # Efeito de pulsação
        pulse = math.sin(self.animation_offset) * 0.2 + 1.0
        size = int(GRID_SIZE * 0.4 * pulse)
        
        # Desenhar com gradiente
        center = (screen_x + GRID_SIZE // 2, screen_y + GRID_SIZE // 2)
        
        # Sombra
        shadow_center = (center[0] + 2, center[1] + 2)
        pygame.draw.circle(surface, (0, 0, 0, 100), shadow_center, size + 2)
        
        # Corpo principal
        pygame.draw.circle(surface, self.color, center, size)
        
        # Brilho interno
        highlight_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(surface, highlight_color, center, size // 2)
        
        # Efeito especial para comidas especiais
        if self.type != "normal":
            # Partículas ao redor
            for i in range(4):
                angle = (pygame.time.get_ticks() * 0.01 + i * math.pi / 2) % (2 * math.pi)
                particle_x = center[0] + math.cos(angle) * (size + 10)
                particle_y = center[1] + math.sin(angle) * (size + 10)
                particle_color = Colors.NEON_BLUE if self.type == "special" else Colors.NEON_PINK
                pygame.draw.circle(surface, particle_color, (int(particle_x), int(particle_y)), 2)

class Snake:
    def __init__(self, start_pos: Position):
        self.body = [start_pos, Position(start_pos.x - 1, start_pos.y)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.grow_pending = 0
        self.speed_boost = 0
        self.invulnerable = 0
        
        # Efeitos visuais
        self.trail_positions = []
        self.body_animations = [0] * len(self.body)
    
    def update(self):
        # Atualizar direção
        self.direction = self.next_direction
        
        # Calcular nova posição da cabeça
        head = self.body[0]
        new_head = Position(
            head.x + self.direction.value[0],
            head.y + self.direction.value[1]
        )
        
        # Adicionar nova cabeça
        self.body.insert(0, new_head)
        self.body_animations.insert(0, 0)
        
        # Adicionar à trilha
        self.trail_positions.append((head.x * GRID_SIZE + GRID_SIZE // 2, 
                                   head.y * GRID_SIZE + GRID_SIZE // 2))
        if len(self.trail_positions) > 10:
            self.trail_positions.pop(0)
        
        # Remover cauda se não estiver crescendo
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
            self.body_animations.pop()
        
        # Atualizar animações
        for i in range(len(self.body_animations)):
            self.body_animations[i] += 0.2
        
        # Decrementar efeitos
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.invulnerable > 0:
            self.invulnerable -= 1
    
    def change_direction(self, new_direction: Direction):
        # Prevenir movimento reverso
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction
    
    def grow(self, amount: int = 1):
        self.grow_pending += amount
    
    def check_collision(self) -> bool:
        head = self.body[0]
        
        # Verificar colisão com paredes
        if (head.x < 0 or head.x >= GRID_WIDTH or 
            head.y < 0 or head.y >= GRID_HEIGHT):
            return True
        
        # Verificar colisão com o próprio corpo (ignorar se invulnerável)
        if self.invulnerable == 0:
            for segment in self.body[1:]:
                if head == segment:
                    return True
        
        return False
    
    def draw(self, surface: pygame.Surface):
        # Desenhar trilha
        for i, pos in enumerate(self.trail_positions):
            alpha = int(50 * (i / len(self.trail_positions)))
            trail_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (*Colors.NEON_GREEN, alpha), (3, 3), 3)
            surface.blit(trail_surface, (pos[0] - 3, pos[1] - 3))
        
        # Desenhar corpo
        for i, segment in enumerate(self.body):
            screen_x = segment.x * GRID_SIZE
            screen_y = segment.y * GRID_SIZE
            
            # Animação de pulsação
            pulse = math.sin(self.body_animations[i]) * 0.1 + 1.0
            size = int(GRID_SIZE * 0.9 * pulse)
            
            # Cor baseada na posição no corpo
            if i == 0:  # Cabeça
                color = Colors.SNAKE_HEAD
                # Efeito de invulnerabilidade
                if self.invulnerable > 0 and self.invulnerable % 10 < 5:
                    color = Colors.NEON_BLUE
            else:  # Corpo
                # Gradiente do corpo para a cauda
                ratio = i / len(self.body)
                color = self.interpolate_color(Colors.SNAKE_BODY, Colors.SNAKE_TAIL, ratio)
            
            # Desenhar sombra
            shadow_rect = pygame.Rect(screen_x + 2, screen_y + 2, size, size)
            pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=size // 4)
            
            # Desenhar segmento principal
            main_rect = pygame.Rect(screen_x + (GRID_SIZE - size) // 2, 
                                  screen_y + (GRID_SIZE - size) // 2, size, size)
            pygame.draw.rect(surface, color, main_rect, border_radius=size // 4)
            
            # Brilho interno
            highlight_size = size // 2
            highlight_rect = pygame.Rect(
                screen_x + (GRID_SIZE - highlight_size) // 2,
                screen_y + (GRID_SIZE - highlight_size) // 2,
                highlight_size, highlight_size
            )
            highlight_color = tuple(min(255, c + 30) for c in color)
            pygame.draw.rect(surface, highlight_color, highlight_rect, border_radius=highlight_size // 4)
            
            # Efeitos especiais
            if self.speed_boost > 0:
                # Efeito de velocidade
                glow_surface = pygame.Surface((size + 10, size + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (*Colors.NEON_BLUE, 50), 
                               (5, 5, size, size), border_radius=size // 4)
                surface.blit(glow_surface, (screen_x - 5, screen_y - 5))
    
    def interpolate_color(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], ratio: float):
        return tuple(int(c1 + (c2 - c1) * ratio) for c1, c2 in zip(color1, color2))

class GameManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 Modern Snake Game")
        self.clock = pygame.time.Clock()
        
        # Fontes
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Estado do jogo
        self.state = GameState.MENU
        self.snake = None
        self.food = None
        self.score = 0
        self.high_score = self.load_high_score()
        self.level = 1
        self.speed = 8  # FPS base
        
        # Efeitos visuais
        self.particles = []
        self.screen_shake = 0
        self.fade_alpha = 0
        
        # Timers
        self.last_move_time = 0
        self.move_delay = 1000 // self.speed  # ms entre movimentos
        
        self.reset_game()
    
    def load_high_score(self) -> int:
        try:
            if os.path.exists("snake_high_score.json"):
                with open("snake_high_score.json", "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except:
            pass
        return 0
    
    def save_high_score(self):
        try:
            with open("snake_high_score.json", "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except:
            pass
    
    def reset_game(self):
        start_pos = Position(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = Snake(start_pos)
        self.spawn_food()
        self.score = 0
        self.level = 1
        self.speed = 8
        self.particles.clear()
        self.screen_shake = 0
    
    def spawn_food(self):
        # Determinar tipo de comida
        rand = random.random()
        if rand < 0.7:  # 70% normal
            food_type = "normal"
        elif rand < 0.9:  # 20% especial
            food_type = "special"
        else:  # 10% bônus
            food_type = "bonus"
        
        # Encontrar posição livre
        while True:
            pos = Position(random.randint(0, GRID_WIDTH - 1), 
                          random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake.body:
                self.food = Food(pos, food_type)
                break
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                
                elif self.state == GameState.PLAYING:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.snake.change_direction(Direction.UP)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_p:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
        
        return True
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        current_time = pygame.time.get_ticks()
        
        # Atualizar comida
        if self.food and not self.food.update():
            self.spawn_food()
        
        # Movimento da cobra baseado em tempo
        if current_time - self.last_move_time >= self.move_delay:
            self.last_move_time = current_time
            
            # Atualizar cobra
            self.snake.update()
            
            # Verificar colisão com comida
            if self.snake.body[0] == self.food.position:
                # Comer comida
                points = self.food.points
                self.score += points
                self.snake.grow(1 if self.food.type == "normal" else 2)
                
                # Efeitos especiais baseados no tipo de comida
                if self.food.type == "special":
                    self.snake.speed_boost = 300  # 5 segundos
                elif self.food.type == "bonus":
                    self.snake.invulnerable = 180  # 3 segundos
                
                # Criar partículas
                food_screen_pos = (self.food.position.x * GRID_SIZE + GRID_SIZE // 2,
                                 self.food.position.y * GRID_SIZE + GRID_SIZE // 2)
                for _ in range(15):
                    color = random.choice(Colors.PARTICLE_COLORS)
                    particle = Particle(food_screen_pos[0], food_screen_pos[1], color)
                    self.particles.append(particle)
                
                # Atualizar velocidade e nível
                if self.score > 0 and self.score % 100 == 0:
                    self.level += 1
                    self.speed = min(20, self.speed + 1)
                    self.move_delay = 1000 // self.speed
                
                # Spawnar nova comida
                self.spawn_food()
                
                # Efeito de tela
                self.screen_shake = 5
            
            # Verificar colisões
            if self.snake.check_collision():
                self.state = GameState.GAME_OVER
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                
                # Efeito de morte
                head_pos = (self.snake.body[0].x * GRID_SIZE + GRID_SIZE // 2,
                           self.snake.body[0].y * GRID_SIZE + GRID_SIZE // 2)
                for _ in range(30):
                    color = random.choice([(255, 0, 0), (255, 100, 0), (255, 200, 0)])
                    particle = Particle(head_pos[0], head_pos[1], color)
                    self.particles.append(particle)
                
                self.screen_shake = 15
        
        # Atualizar partículas
        self.particles = [p for p in self.particles if p.update()]
        
        # Atualizar efeitos
        if self.screen_shake > 0:
            self.screen_shake -= 1
    
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, Colors.GRID_LINE, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, Colors.GRID_LINE, (0, y), (WINDOW_WIDTH, y))
    
    def draw_ui(self):
        # Painel superior
        ui_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 60)
        pygame.draw.rect(self.screen, Colors.UI_BACKGROUND, ui_rect)
        pygame.draw.rect(self.screen, Colors.UI_BORDER, ui_rect, 2)
        
        # Pontuação
        score_text = self.font_medium.render(f"Pontuação: {self.score}", True, Colors.TEXT_PRIMARY)
        self.screen.blit(score_text, (20, 15))
        
        # Recorde
        high_score_text = self.font_small.render(f"Recorde: {self.high_score}", True, Colors.TEXT_SECONDARY)
        self.screen.blit(high_score_text, (20, 35))
        
        # Nível
        level_text = self.font_medium.render(f"Nível: {self.level}", True, Colors.TEXT_PRIMARY)
        level_rect = level_text.get_rect()
        level_rect.centerx = WINDOW_WIDTH // 2
        level_rect.y = 15
        self.screen.blit(level_text, level_rect)
        
        # Velocidade
        speed_text = self.font_small.render(f"Velocidade: {self.speed}", True, Colors.TEXT_SECONDARY)
        speed_rect = speed_text.get_rect()
        speed_rect.centerx = WINDOW_WIDTH // 2
        speed_rect.y = 35
        self.screen.blit(speed_text, speed_rect)
        
        # Status da cobra
        status_x = WINDOW_WIDTH - 200
        if self.snake.speed_boost > 0:
            boost_text = self.font_small.render("VELOCIDADE!", True, Colors.NEON_BLUE)
            self.screen.blit(boost_text, (status_x, 15))
        
        if self.snake.invulnerable > 0:
            invul_text = self.font_small.render("INVULNERÁVEL!", True, Colors.NEON_PINK)
            self.screen.blit(invul_text, (status_x, 35))
    
    def draw_menu(self):
        # Fundo com gradiente
        for y in range(WINDOW_HEIGHT):
            color_ratio = y / WINDOW_HEIGHT
            color = tuple(int(Colors.BACKGROUND[i] + (Colors.UI_BACKGROUND[i] - Colors.BACKGROUND[i]) * color_ratio) 
                         for i in range(3))
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
        
        # Título
        title_text = self.font_large.render("🐍 MODERN SNAKE", True, Colors.NEON_GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.font_medium.render("Jogo da Cobrinha Modernizado", True, Colors.TEXT_SECONDARY)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Instruções
        instructions = [
            "ESPAÇO - Iniciar Jogo",
            "WASD ou Setas - Mover",
            "P - Pausar",
            "ESC - Menu Principal"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, Colors.TEXT_PRIMARY)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20 + i * 30))
            self.screen.blit(text, text_rect)
        
        # Recorde
        if self.high_score > 0:
            record_text = self.font_medium.render(f"Recorde Atual: {self.high_score}", True, Colors.NEON_BLUE)
            record_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
            self.screen.blit(record_text, record_rect)
    
    def draw_game_over(self):
        # Overlay escuro
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Texto principal
        game_over_text = self.font_large.render("GAME OVER", True, Colors.FOOD_NORMAL)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Pontuação final
        final_score_text = self.font_medium.render(f"Pontuação Final: {self.score}", True, Colors.TEXT_PRIMARY)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Novo recorde
        if self.score == self.high_score and self.score > 0:
            new_record_text = self.font_medium.render("🏆 NOVO RECORDE! 🏆", True, Colors.NEON_GREEN)
            new_record_rect = new_record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(new_record_text, new_record_rect)
        
        # Instruções
        restart_text = self.font_small.render("ESPAÇO - Jogar Novamente", True, Colors.TEXT_SECONDARY)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_small.render("ESC - Menu Principal", True, Colors.TEXT_SECONDARY)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_paused(self):
        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))
        
        # Texto de pausa
        paused_text = self.font_large.render("PAUSADO", True, Colors.NEON_BLUE)
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(paused_text, paused_rect)
        
        # Instruções
        continue_text = self.font_small.render("P - Continuar", True, Colors.TEXT_PRIMARY)
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(continue_text, continue_rect)
    
    def draw(self):
        # Aplicar shake da tela
        shake_offset = (0, 0)
        if self.screen_shake > 0:
            shake_offset = (random.randint(-self.screen_shake, self.screen_shake),
                          random.randint(-self.screen_shake, self.screen_shake))
        
        # Limpar tela
        self.screen.fill(Colors.BACKGROUND)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        
        elif self.state in [GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER]:
            # Desenhar grade
            self.draw_grid()
            
            # Desenhar elementos do jogo
            if self.food:
                self.food.draw(self.screen)
            
            if self.snake:
                self.snake.draw(self.screen)
            
            # Desenhar partículas
            for particle in self.particles:
                particle.draw(self.screen)
            
            # Desenhar UI
            self.draw_ui()
            
            # Overlays baseados no estado
            if self.state == GameState.PAUSED:
                self.draw_paused()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
        
        # Aplicar shake se necessário
        if shake_offset != (0, 0):
            # Criar superfície temporária e aplicar offset
            temp_surface = self.screen.copy()
            self.screen.fill(Colors.BACKGROUND)
            self.screen.blit(temp_surface, shake_offset)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

# Executar o jogo
if __name__ == "__main__":
    game = GameManager()
    game.run()
