import pygame
import random
import sys
import math
from pygame import gfxdraw

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Shooter - Enhanced Edition")

# Cores aprimoradas
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (30, 144, 255)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 100)
PURPLE = (138, 43, 226)
CYAN = (0, 255, 255)
DARK_BLUE = (25, 25, 112)
SPACE_BLUE = (10, 10, 40)
NEON_GREEN = (57, 255, 20)
NEON_PINK = (255, 20, 147)

# Classe para partículas de fundo (estrelas)
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.5, 3)
        self.brightness = random.randint(100, 255)
        self.size = random.choice([1, 1, 1, 2, 2, 3])  # Mais estrelas pequenas
        self.twinkle_speed = random.uniform(0.02, 0.1)
        self.twinkle_offset = random.uniform(0, math.pi * 2)
    
    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT)
        
        # Efeito de cintilação
        self.brightness = int(150 + 105 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_offset))
    
    def draw(self, surface):
        color = (self.brightness, self.brightness, self.brightness)
        if self.size == 1:
            pygame.draw.rect(surface, color, (int(self.x), int(self.y), 1, 1))
        else:
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

# Classe do jogador (nave) aprimorada
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = self.create_ship()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 6
        self.rect.centery = HEIGHT // 2
        self.speed_x = 0
        self.speed_y = 0
        self.max_speed = 7
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()
        self.health = 100
        self.max_health = 100
        self.shield = 0
        self.max_shield = 50
        
        # Efeitos visuais
        self.engine_particles = []
        self.hit_flash = 0
        self.invulnerable_time = 0
        
        # Power-ups
        self.rapid_fire = 0
        self.double_shot = 0
        self.triple_shot = 0
    
    def create_ship(self):
        # Criar uma nave mais detalhada
        ship = pygame.Surface((60, 40), pygame.SRCALPHA)
        
        # Corpo principal (gradiente)
        for i in range(40):
            color_intensity = int(200 - i * 2)
            color = (color_intensity, color_intensity, min(255, color_intensity + 50))
            pygame.draw.rect(ship, color, (15, i, 30, 1))
        
        # Asas
        wing_points = [(10, 10), (15, 5), (45, 15), (50, 20), (45, 25), (15, 35), (10, 30)]
        pygame.draw.polygon(ship, (150, 150, 200), wing_points)
        pygame.draw.polygon(ship, (100, 100, 150), wing_points, 2)
        
        # Cockpit
        pygame.draw.ellipse(ship, CYAN, (35, 15, 15, 10))
        pygame.draw.ellipse(ship, WHITE, (37, 17, 11, 6))
        
        # Motores
        pygame.draw.ellipse(ship, (80, 80, 80), (5, 12, 8, 6))
        pygame.draw.ellipse(ship, (80, 80, 80), (5, 22, 8, 6))
        
        # Detalhes
        pygame.draw.line(ship, NEON_GREEN, (20, 10), (40, 15), 2)
        pygame.draw.line(ship, NEON_GREEN, (20, 30), (40, 25), 2)
        
        return ship
    
    def update(self):
        # Movimento suave
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = max(self.speed_x - 0.5, -self.max_speed)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = min(self.speed_x + 0.5, self.max_speed)
        else:
            self.speed_x *= 0.9
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed_y = max(self.speed_y - 0.5, -self.max_speed)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed_y = min(self.speed_y + 0.5, self.max_speed)
        else:
            self.speed_y *= 0.9
        
        # Atualizar posição
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Manter na tela
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        
        # Atualizar efeitos
        self.update_engine_particles()
        
        if self.hit_flash > 0:
            self.hit_flash -= 1
            
        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1
            
        # Decrementar power-ups
        if self.rapid_fire > 0:
            self.rapid_fire -= 1
        if self.double_shot > 0:
            self.double_shot -= 1
        if self.triple_shot > 0:
            self.triple_shot -= 1
        
        # Regenerar escudo lentamente
        if self.shield < self.max_shield:
            self.shield += 0.1
    
    def update_engine_particles(self):
        # Adicionar partículas do motor
        if len(self.engine_particles) < 20:
            for _ in range(2):
                particle = {
                    'x': self.rect.left - 5,
                    'y': self.rect.centery + random.randint(-8, 8),
                    'vx': random.uniform(-3, -1),
                    'vy': random.uniform(-1, 1),
                    'life': random.randint(10, 20),
                    'color': random.choice([ORANGE, YELLOW, RED])
                }
                self.engine_particles.append(particle)
        
        # Atualizar partículas
        for particle in self.engine_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.engine_particles.remove(particle)
    
    def draw_engine_particles(self, surface):
        for particle in self.engine_particles:
            alpha = int(255 * (particle['life'] / 20))
            color = (*particle['color'], alpha)
            size = max(1, particle['life'] // 4)
            pygame.draw.circle(surface, particle['color'], 
                             (int(particle['x']), int(particle['y'])), size)
    
    def shoot(self):
        now = pygame.time.get_ticks()
        delay = self.shoot_delay // 2 if self.rapid_fire > 0 else self.shoot_delay
        
        if now - self.last_shot > delay:
            self.last_shot = now
            
            if self.triple_shot > 0:
                # Tiro triplo
                bullets_created = [
                    Bullet(self.rect.right, self.rect.centery - 10, angle=-10),
                    Bullet(self.rect.right, self.rect.centery, angle=0),
                    Bullet(self.rect.right, self.rect.centery + 10, angle=10)
                ]
            elif self.double_shot > 0:
                # Tiro duplo
                bullets_created = [
                    Bullet(self.rect.right, self.rect.centery - 5),
                    Bullet(self.rect.right, self.rect.centery + 5)
                ]
            else:
                # Tiro simples
                bullets_created = [Bullet(self.rect.right, self.rect.centery)]
            
            for bullet in bullets_created:
                all_sprites.add(bullet)
                bullets.add(bullet)
            
            return True
        return False
    
    def take_damage(self, damage):
        if self.invulnerable_time > 0:
            return False
            
        if self.shield > 0:
            shield_damage = min(damage, self.shield)
            self.shield -= shield_damage
            damage -= shield_damage
        
        if damage > 0:
            self.health -= damage
            self.hit_flash = 10
            self.invulnerable_time = 60
        
        return True
    
    def draw(self, surface):
        # Desenhar partículas do motor primeiro
        self.draw_engine_particles(surface)
        
        # Efeito de piscar quando invulnerável
        if self.invulnerable_time > 0 and self.invulnerable_time % 10 < 5:
            return
        
        # Efeito de flash quando atingido
        if self.hit_flash > 0:
            flash_surface = self.original_image.copy()
            flash_surface.fill((255, 255, 255, 100), special_flags=pygame.BLEND_ADD)
            surface.blit(flash_surface, self.rect)
        else:
            surface.blit(self.image, self.rect)

# Classe de projéteis aprimorada
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0, bullet_type="normal"):
        super().__init__()
        self.bullet_type = bullet_type
        self.angle = angle
        
        if bullet_type == "laser":
            self.image = self.create_laser()
            self.speed = 15
            self.damage = 2
        else:
            self.image = self.create_bullet()
            self.speed = 12
            self.damage = 1
        
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        
        # Calcular velocidade baseada no ângulo
        self.vx = self.speed * math.cos(math.radians(angle))
        self.vy = self.speed * math.sin(math.radians(angle))
        
        self.trail = []
    
    def create_bullet(self):
        bullet = pygame.Surface((12, 4), pygame.SRCALPHA)
        # Gradiente de cor
        for i in range(12):
            intensity = int(255 * (i / 12))
            color = (255, intensity, 0)
            pygame.draw.rect(bullet, color, (i, 0, 1, 4))
        
        # Brilho
        pygame.draw.rect(bullet, YELLOW, (8, 1, 4, 2))
        return bullet
    
    def create_laser(self):
        laser = pygame.Surface((20, 3), pygame.SRCALPHA)
        pygame.draw.rect(laser, NEON_GREEN, (0, 0, 20, 3))
        pygame.draw.rect(laser, WHITE, (0, 1, 20, 1))
        return laser
    
    def update(self):
        # Adicionar posição atual ao rastro
        self.trail.append((self.rect.centerx, self.rect.centery))
        if len(self.trail) > 5:
            self.trail.pop(0)
        
        # Mover projétil
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Remover se sair da tela
        if (self.rect.right < 0 or self.rect.left > WIDTH or 
            self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()
    
    def draw(self, surface):
        # Desenhar rastro
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            color = (*ORANGE, alpha) if self.bullet_type == "normal" else (*NEON_GREEN, alpha)
            size = max(1, i)
            pygame.draw.circle(surface, ORANGE if self.bullet_type == "normal" else NEON_GREEN, 
                             pos, size)
        
        # Desenhar projétil
        surface.blit(self.image, self.rect)

# Classe de inimigos aprimorada
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type="basic"):
        super().__init__()
        self.enemy_type = enemy_type
        self.health = self.get_health()
        self.max_health = self.health
        self.image = self.create_enemy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH, WIDTH + 200)
        self.rect.y = random.randrange(50, HEIGHT - 100)
        self.speed = self.get_speed()
        self.shoot_delay = random.randrange(1000, 3000)
        self.last_shot = pygame.time.get_ticks()
        
        # Movimento
        self.angle = 0
        self.amplitude = random.randrange(20, 60)
        self.original_y = self.rect.y
        
        # Efeitos
        self.hit_flash = 0
    
    def get_health(self):
        health_map = {"basic": 1, "fighter": 2, "heavy": 4, "boss": 10}
        return health_map.get(self.enemy_type, 1)
    
    def get_speed(self):
        speed_map = {"basic": random.randrange(2, 4), "fighter": random.randrange(3, 6), 
                    "heavy": random.randrange(1, 3), "boss": random.randrange(1, 2)}
        return speed_map.get(self.enemy_type, 2)
    
    def create_enemy(self):
        if self.enemy_type == "basic":
            return self.create_basic_enemy()
        elif self.enemy_type == "fighter":
            return self.create_fighter_enemy()
        elif self.enemy_type == "heavy":
            return self.create_heavy_enemy()
        elif self.enemy_type == "boss":
            return self.create_boss_enemy()
    
    def create_basic_enemy(self):
        enemy = pygame.Surface((30, 25), pygame.SRCALPHA)
        # Corpo principal
        pygame.draw.ellipse(enemy, RED, (5, 5, 20, 15))
        pygame.draw.ellipse(enemy, (150, 0, 0), (5, 5, 20, 15), 2)
        # Asas
        pygame.draw.polygon(enemy, (100, 0, 0), [(0, 10), (5, 5), (5, 20), (0, 15)])
        pygame.draw.polygon(enemy, (100, 0, 0), [(25, 5), (30, 10), (30, 15), (25, 20)])
        # Cockpit
        pygame.draw.circle(enemy, YELLOW, (15, 12), 3)
        return enemy
    
    def create_fighter_enemy(self):
        enemy = pygame.Surface((35, 30), pygame.SRCALPHA)
        # Corpo
        pygame.draw.polygon(enemy, PURPLE, [(5, 15), (15, 5), (25, 10), (30, 15), (25, 20), (15, 25)])
        pygame.draw.polygon(enemy, (100, 0, 100), [(5, 15), (15, 5), (25, 10), (30, 15), (25, 20), (15, 25)], 2)
        # Motores
        pygame.draw.circle(enemy, ORANGE, (8, 10), 3)
        pygame.draw.circle(enemy, ORANGE, (8, 20), 3)
        return enemy
    
    def create_heavy_enemy(self):
        enemy = pygame.Surface((45, 35), pygame.SRCALPHA)
        # Corpo principal
        pygame.draw.rect(enemy, (100, 100, 100), (10, 10, 25, 15))
        pygame.draw.rect(enemy, (150, 150, 150), (10, 10, 25, 15), 3)
        # Canhões
        pygame.draw.rect(enemy, (80, 80, 80), (5, 12, 8, 3))
        pygame.draw.rect(enemy, (80, 80, 80), (5, 20, 8, 3))
        # Detalhes
        pygame.draw.circle(enemy, RED, (22, 17), 4)
        return enemy
    
    def create_boss_enemy(self):
        enemy = pygame.Surface((80, 60), pygame.SRCALPHA)
        # Corpo principal
        pygame.draw.ellipse(enemy, (50, 0, 50), (10, 15, 60, 30))
        pygame.draw.ellipse(enemy, PURPLE, (10, 15, 60, 30), 4)
        # Asas
        pygame.draw.polygon(enemy, (80, 0, 80), [(0, 20), (15, 10), (15, 50), (0, 40)])
        pygame.draw.polygon(enemy, (80, 0, 80), [(65, 10), (80, 20), (80, 40), (65, 50)])
        # Centro
        pygame.draw.circle(enemy, RED, (40, 30), 8)
        pygame.draw.circle(enemy, YELLOW, (40, 30), 4)
        return enemy
    
    def update(self):
        # Movimento
        self.rect.x -= self.speed
        
        # Movimento senoidal para alguns tipos
        if self.enemy_type in ["fighter", "boss"]:
            self.angle += 2
            self.rect.y = self.original_y + int(math.sin(math.radians(self.angle)) * self.amplitude)
        
        # Atirar ocasionalmente
        if self.enemy_type in ["fighter", "heavy", "boss"]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot_delay = random.randrange(1500, 4000)
                self.shoot_at_player()
        
        # Reposicionar se sair da tela
        if self.rect.right < 0:
            self.rect.x = random.randrange(WIDTH, WIDTH + 200)
            self.original_y = random.randrange(50, HEIGHT - 100)
            self.rect.y = self.original_y
            self.health = self.max_health
        
        # Atualizar efeitos
        if self.hit_flash > 0:
            self.hit_flash -= 1
    
    def shoot_at_player(self):
        # Calcular ângulo para o jogador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        
        # Criar projétil inimigo
        enemy_bullet = EnemyBullet(self.rect.left, self.rect.centery, angle)
        all_sprites.add(enemy_bullet)
        enemy_bullets.add(enemy_bullet)
    
    def take_damage(self, damage):
        self.health -= damage
        self.hit_flash = 5
        return self.health <= 0
    
    def draw(self, surface):
        # Efeito de flash quando atingido
        if self.hit_flash > 0:
            flash_surface = self.image.copy()
            flash_surface.fill((255, 255, 255, 100), special_flags=pygame.BLEND_ADD)
            surface.blit(flash_surface, self.rect)
        else:
            surface.blit(self.image, self.rect)
        
        # Barra de vida para inimigos mais fortes
        if self.enemy_type in ["heavy", "boss"] and self.health < self.max_health:
            bar_width = self.rect.width
            bar_height = 4
            health_ratio = self.health / self.max_health
            
            pygame.draw.rect(surface, RED, 
                           (self.rect.x, self.rect.y - 8, bar_width, bar_height))
            pygame.draw.rect(surface, GREEN, 
                           (self.rect.x, self.rect.y - 8, bar_width * health_ratio, bar_height))

# Classe de projéteis inimigos
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (4, 4), 4)
        pygame.draw.circle(self.image, ORANGE, (4, 4), 2)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.speed = 6
        self.vx = self.speed * math.cos(math.radians(angle))
        self.vy = self.speed * math.sin(math.radians(angle))
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        if (self.rect.right < 0 or self.rect.left > WIDTH or 
            self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()

# Classe de power-ups
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.power_type = random.choice(["health", "shield", "rapid_fire", "double_shot", "triple_shot"])
        self.image = self.create_powerup()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 2
        self.bob_offset = random.uniform(0, math.pi * 2)
        self.original_y = y
    
    def create_powerup(self):
        powerup = pygame.Surface((25, 25), pygame.SRCALPHA)
        
        if self.power_type == "health":
            pygame.draw.circle(powerup, GREEN, (12, 12), 10)
            pygame.draw.rect(powerup, WHITE, (10, 6, 4, 12))
            pygame.draw.rect(powerup, WHITE, (6, 10, 12, 4))
        elif self.power_type == "shield":
            pygame.draw.circle(powerup, CYAN, (12, 12), 10)
            pygame.draw.circle(powerup, WHITE, (12, 12), 6)
        elif self.power_type == "rapid_fire":
            pygame.draw.circle(powerup, YELLOW, (12, 12), 10)
            pygame.draw.polygon(powerup, RED, [(8, 12), (16, 8), (16, 16)])
        elif self.power_type == "double_shot":
            pygame.draw.circle(powerup, ORANGE, (12, 12), 10)
            pygame.draw.circle(powerup, WHITE, (8, 12), 2)
            pygame.draw.circle(powerup, WHITE, (16, 12), 2)
        elif self.power_type == "triple_shot":
            pygame.draw.circle(powerup, PURPLE, (12, 12), 10)
            pygame.draw.circle(powerup, WHITE, (6, 12), 2)
            pygame.draw.circle(powerup, WHITE, (12, 12), 2)
            pygame.draw.circle(powerup, WHITE, (18, 12), 2)
        
        return powerup
    
    def update(self):
        self.rect.x -= self.speed
        
        # Efeito de flutuação
        self.rect.y = self.original_y + int(math.sin(pygame.time.get_ticks() * 0.005 + self.bob_offset) * 5)
        
        if self.rect.right < 0:
            self.kill()
    
    def apply_effect(self, player):
        if self.power_type == "health":
            player.health = min(player.max_health, player.health + 25)
        elif self.power_type == "shield":
            player.shield = min(player.max_shield, player.shield + 25)
        elif self.power_type == "rapid_fire":
            player.rapid_fire = 600  # 10 segundos a 60 FPS
        elif self.power_type == "double_shot":
            player.double_shot = 600
        elif self.power_type == "triple_shot":
            player.triple_shot = 600

# Classe de explosões
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size="medium"):
        super().__init__()
        self.size = size
        self.frame = 0
        self.max_frames = 15
        self.images = self.create_explosion_frames()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame_rate = 2
        self.frame_counter = 0
    
    def create_explosion_frames(self):
        frames = []
        sizes = {"small": 30, "medium": 50, "large": 80}
        max_size = sizes.get(self.size, 50)
        
        for frame in range(self.max_frames):
            surface = pygame.Surface((max_size, max_size), pygame.SRCALPHA)
            progress = frame / self.max_frames
            
            # Círculo principal
            radius = int(max_size * 0.4 * (1 - progress * 0.5))
            if radius > 0:
                color_intensity = int(255 * (1 - progress))
                colors = [
                    (255, color_intensity, 0),
                    (255, color_intensity // 2, 0),
                    (color_intensity, 0, 0)
                ]
                
                for i, color in enumerate(colors):
                    r = radius - i * 3
                    if r > 0:
                        pygame.draw.circle(surface, color, (max_size // 2, max_size // 2), r)
            
            # Partículas
            for _ in range(int(20 * (1 - progress))):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, max_size * 0.3)
                x = max_size // 2 + int(math.cos(angle) * distance)
                y = max_size // 2 + int(math.sin(angle) * distance)
                
                if 0 <= x < max_size and 0 <= y < max_size:
                    particle_color = random.choice([ORANGE, YELLOW, RED])
                    pygame.draw.circle(surface, particle_color, (x, y), random.randint(1, 3))
            
            frames.append(surface)
        
        return frames
    
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.frame += 1
            
            if self.frame >= self.max_frames:
                self.kill()
            else:
                self.image = self.images[self.frame]

# Classe do fundo com paralaxe
class Background:
    def __init__(self):
        self.stars = [Star() for _ in range(200)]
        self.nebula_particles = []
        self.create_nebula()
    
    def create_nebula(self):
        for _ in range(50):
            particle = {
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.randint(20, 80),
                'color': random.choice([DARK_BLUE, PURPLE, (50, 0, 100)]),
                'alpha': random.randint(20, 60),
                'speed': random.uniform(0.1, 0.5)
            }
            self.nebula_particles.append(particle)
    
    def update(self):
        for star in self.stars:
            star.update()
        
        for particle in self.nebula_particles:
            particle['x'] -= particle['speed']
            if particle['x'] < -particle['size']:
                particle['x'] = WIDTH + particle['size']
    
    def draw(self, surface):
        # Fundo base
        surface.fill(SPACE_BLUE)
        
        # Nebulosa
        for particle in self.nebula_particles:
            s = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(s, (*particle['color'], particle['alpha']), 
                             (particle['size'] // 2, particle['size'] // 2), 
                             particle['size'] // 2)
            surface.blit(s, (particle['x'], particle['y']))
        
        # Estrelas
        for star in self.stars:
            star.draw(surface)

# Classe da interface do usuário
class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
    
    def draw_hud(self, surface, player, score, wave):
        # Barra de vida
        health_ratio = player.health / player.max_health
        health_color = GREEN if health_ratio > 0.6 else YELLOW if health_ratio > 0.3 else RED
        
        pygame.draw.rect(surface, (50, 50, 50), (20, 20, 200, 20))
        pygame.draw.rect(surface, health_color, (20, 20, 200 * health_ratio, 20))
        pygame.draw.rect(surface, WHITE, (20, 20, 200, 20), 2)
        
        health_text = self.font_small.render("VIDA", True, WHITE)
        surface.blit(health_text, (20, 45))
        
        # Barra de escudo
        if player.shield > 0:
            shield_ratio = player.shield / player.max_shield
            pygame.draw.rect(surface, (20, 20, 50), (20, 70, 200, 15))
            pygame.draw.rect(surface, CYAN, (20, 70, 200 * shield_ratio, 15))
            pygame.draw.rect(surface, WHITE, (20, 70, 200, 15), 2)
            
            shield_text = self.font_small.render("ESCUDO", True, WHITE)
            surface.blit(shield_text, (20, 90))
        
        # Pontuação
        score_text = self.font_medium.render(f"PONTUAÇÃO: {score}", True, WHITE)
        surface.blit(score_text, (WIDTH - 250, 20))
        
        # Onda
        wave_text = self.font_medium.render(f"ONDA: {wave}", True, WHITE)
        surface.blit(wave_text, (WIDTH - 250, 60))
        
        # Power-ups ativos
        y_offset = 120
        if player.rapid_fire > 0:
            rapid_text = self.font_small.render("TIRO RÁPIDO", True, YELLOW)
            surface.blit(rapid_text, (20, y_offset))
            y_offset += 25
        
        if player.double_shot > 0:
            double_text = self.font_small.render("TIRO DUPLO", True, ORANGE)
            surface.blit(double_text, (20, y_offset))
            y_offset += 25
        
        if player.triple_shot > 0:
            triple_text = self.font_small.render("TIRO TRIPLO", True, PURPLE)
            surface.blit(triple_text, (20, y_offset))
    
    def draw_game_over(self, surface, score, high_score):
        # Overlay escuro
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        # Texto principal
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        surface.blit(game_over_text, text_rect)
        
        # Pontuação
        score_text = self.font_medium.render(f"Pontuação Final: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        surface.blit(score_text, score_rect)
        
        # Recorde
        if score >= high_score:
            new_record_text = self.font_medium.render("NOVO RECORDE!", True, YELLOW)
            record_rect = new_record_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
            surface.blit(new_record_text, record_rect)
        else:
            high_score_text = self.font_medium.render(f"Recorde: {high_score}", True, WHITE)
            high_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
            surface.blit(high_score_text, high_rect)
        
        # Instruções
        restart_text = self.font_small.render("Pressione R para reiniciar ou ESC para sair", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        surface.blit(restart_text, restart_rect)

# Inicializar grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Criar objetos do jogo
player = Player()
all_sprites.add(player)
background = Background()
ui = UI()

# Variáveis do jogo
clock = pygame.time.Clock()
score = 0
high_score = 0
wave = 1
enemies_spawned = 0
enemies_per_wave = 10
last_enemy_spawn = 0
enemy_spawn_delay = 2000
last_powerup_spawn = 0
powerup_spawn_delay = 15000

# Estados do jogo
running = True
game_over = False
paused = False

# Loop principal do jogo
while running:
    dt = clock.tick(60)
    
    # Processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_r and game_over:
                # Reiniciar jogo
                game_over = False
                player.health = player.max_health
                player.shield = 0
                player.rect.centerx = WIDTH // 6
                player.rect.centery = HEIGHT // 2
                score = 0
                wave = 1
                enemies_spawned = 0
                
                # Limpar sprites
                for sprite in enemies:
                    sprite.kill()
                for sprite in bullets:
                    sprite.kill()
                for sprite in enemy_bullets:
                    sprite.kill()
                for sprite in powerups:
                    sprite.kill()
                for sprite in explosions:
                    sprite.kill()
    
    if not game_over and not paused:
        # Controles contínuos
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        # Spawnar inimigos
        now = pygame.time.get_ticks()
        if (now - last_enemy_spawn > enemy_spawn_delay and 
            enemies_spawned < enemies_per_wave):
            
            # Determinar tipo de inimigo baseado na onda
            if wave >= 5 and random.random() < 0.1:
                enemy_type = "boss"
            elif wave >= 3 and random.random() < 0.3:
                enemy_type = "heavy"
            elif wave >= 2 and random.random() < 0.4:
                enemy_type = "fighter"
            else:
                enemy_type = "basic"
            
            enemy = Enemy(enemy_type)
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemies_spawned += 1
            last_enemy_spawn = now
            
            # Ajustar delay baseado na onda
            enemy_spawn_delay = max(500, 2000 - wave * 100)
        
        # Verificar se a onda terminou
        if enemies_spawned >= enemies_per_wave and len(enemies) == 0:
            wave += 1
            enemies_spawned = 0
            enemies_per_wave += 2
            
            # Spawnar power-up de bônus de onda
            powerup = PowerUp(WIDTH - 50, HEIGHT // 2)
            all_sprites.add(powerup)
            powerups.add(powerup)
        
        # Spawnar power-ups ocasionalmente
        if now - last_powerup_spawn > powerup_spawn_delay:
            if random.random() < 0.3:  # 30% de chance
                powerup = PowerUp(WIDTH - 50, random.randint(50, HEIGHT - 50))
                all_sprites.add(powerup)
                powerups.add(powerup)
            last_powerup_spawn = now
        
        # Atualizar sprites
        all_sprites.update()
        background.update()
        
        # Colisões: projéteis do jogador vs inimigos
        for bullet in bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_enemies:
                bullet.kill()
                if enemy.take_damage(bullet.damage):
                    # Inimigo morreu
                    explosion = Explosion(enemy.rect.center, 
                                        "large" if enemy.enemy_type == "boss" else "medium")
                    all_sprites.add(explosion)
                    explosions.add(explosion)
                    
                    score += {"basic": 10, "fighter": 20, "heavy": 30, "boss": 100}[enemy.enemy_type]
                    
                    # Chance de dropar power-up
                    if random.random() < 0.15:
                        powerup = PowerUp(enemy.rect.centerx, enemy.rect.centery)
                        all_sprites.add(powerup)
                        powerups.add(powerup)
                    
                    enemy.kill()
        
        # Colisões: projéteis inimigos vs jogador
        hit_bullets = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for bullet in hit_bullets:
            if player.take_damage(5):
                explosion = Explosion(player.rect.center, "small")
                all_sprites.add(explosion)
                explosions.add(explosion)
        
        # Colisões: jogador vs inimigos
        hit_enemies = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in hit_enemies:
            if player.take_damage(10):
                explosion = Explosion(player.rect.center, "medium")
                all_sprites.add(explosion)
                explosions.add(explosion)
            
            # Inimigo também toma dano
            if enemy.take_damage(2):
                explosion = Explosion(enemy.rect.center, "medium")
                all_sprites.add(explosion)
                explosions.add(explosion)
                enemy.kill()
        
        # Colisões: jogador vs power-ups
        collected_powerups = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in collected_powerups:
            powerup.apply_effect(player)
        
        # Verificar game over
        if player.health <= 0:
            game_over = True
            if score > high_score:
                high_score = score
            
            # Explosão final
            explosion = Explosion(player.rect.center, "large")
            all_sprites.add(explosion)
            explosions.add(explosion)
    
    # Renderização
    background.draw(screen)
    
    # Desenhar sprites customizados
    for sprite in all_sprites:
        if hasattr(sprite, 'draw'):
            sprite.draw(screen)
        else:
            screen.blit(sprite.image, sprite.rect)
    
    # Interface do usuário
    if not game_over:
        ui.draw_hud(screen, player, score, wave)
    else:
        ui.draw_game_over(screen, score, high_score)
    
    # Tela de pausa
    if paused and not game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        
        pause_text = ui.font_large.render("PAUSADO", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(pause_text, pause_rect)
        
        continue_text = ui.font_small.render("Pressione P para continuar", True, WHITE)
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(continue_text, continue_rect)
    
    pygame.display.flip()

# Encerrar
pygame.quit()
sys.exit()
