import pygame
import random
import sys
import math
from pygame import gfxdraw

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Pixel Art")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
WATER_BLUE = (65, 105, 225)
ROCK_BROWN = (139, 69, 19)

# Função para criar uma superfície com pixel art
def create_pixel_surface(width, height, pixel_size=1):
    surf = pygame.Surface((width * pixel_size, height * pixel_size))
    surf.fill((0, 0, 0, 0))
    return surf

# Classe do jogador (nave)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Criar uma nave com pixel art
        self.pixel_size = 2
        self.width, self.height = 25, 15
        self.image = create_pixel_surface(self.width, self.height, self.pixel_size)
        
        # Desenhar a nave em estilo pixel art
        # Corpo principal
        for x in range(5, 20):
            for y in range(5, 10):
                pygame.draw.rect(self.image, (200, 50, 50), 
                                (x * self.pixel_size, y * self.pixel_size, 
                                 self.pixel_size, self.pixel_size))
        
        # Asas
        for x in range(10, 15):
            for y in range(2, 5):
                pygame.draw.rect(self.image, (150, 150, 150), 
                                (x * self.pixel_size, y * self.pixel_size, 
                                 self.pixel_size, self.pixel_size))
            for y in range(10, 13):
                pygame.draw.rect(self.image, (150, 150, 150), 
                                (x * self.pixel_size, y * self.pixel_size, 
                                 self.pixel_size, self.pixel_size))
        
        # Cockpit
        for x in range(15, 18):
            for y in range(6, 9):
                pygame.draw.rect(self.image, (100, 200, 255), 
                                (x * self.pixel_size, y * self.pixel_size, 
                                 self.pixel_size, self.pixel_size))
        
        # Motor
        for x in range(2, 5):
            for y in range(6, 9):
                pygame.draw.rect(self.image, ORANGE, 
                                (x * self.pixel_size, y * self.pixel_size, 
                                 self.pixel_size, self.pixel_size))
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.bottom = HEIGHT - 50
        self.speed_x = 0
        self.speed_y = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.health = 100
        
        # Animação do motor
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        # Atualizar posição baseada na velocidade
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Manter a nave dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
            
        # Animar o motor
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = (self.frame + 1) % 3
            
            # Redesenhar o motor com animação
            for x in range(2, 5):
                for y in range(6, 9):
                    color = BLACK
                    pygame.draw.rect(self.image, color, 
                                    (x * self.pixel_size, y * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))
            
            flame_length = 3 + self.frame
            for x in range(0, flame_length):
                for y in range(6, 9):
                    color = ORANGE if x > 0 else (255, 255, 200)
                    pygame.draw.rect(self.image, color, 
                                    ((4-x) * self.pixel_size, y * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
            return True
        return False

# Classe dos projéteis
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pixel_size = 2
        self.width, self.height = 5, 3
        self.image = create_pixel_surface(self.width, self.height, self.pixel_size)
        
        # Desenhar o projétil em estilo pixel art
        for x in range(self.width):
            for y in range(self.height):
                if x == 0 or y == 0 or x == self.width-1 or y == self.height-1:
                    color = (255, 200, 0)  # Borda
                else:
                    color = (255, 100, 0)  # Centro
                pygame.draw.rect(self.image, color, 
                                (x * self.pixel_size, y * self.pixel_size, 
                                 self.pixel_size, self.pixel_size))
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        # Remover o projétil se sair da tela
        if self.rect.left > WIDTH:
            self.kill()

# Classe dos inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pixel_size = 2
        self.width, self.height = 15, 15
        self.image = create_pixel_surface(self.width, self.height, self.pixel_size)
        
        # Desenhar o inimigo em estilo pixel art
        enemy_type = random.choice(["ufo", "ship"])
        
        if enemy_type == "ufo":
            # Corpo do UFO
            for x in range(3, 12):
                for y in range(6, 9):
                    pygame.draw.rect(self.image, (150, 150, 150), 
                                    (x * self.pixel_size, y * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))
            
            # Cúpula do UFO
            for x in range(5, 10):
                for y in range(3, 6):
                    pygame.draw.rect(self.image, (100, 200, 100), 
                                    (x * self.pixel_size, y * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))
            
            # Luzes do UFO
            for x in range(4, 12, 2):
                pygame.draw.rect(self.image, (255, 255, 0), 
                                (x * self.pixel_size, 9 * self.pixel_size, 
                                 self.pixel_size, self.pixel_size))
        else:
            # Corpo da nave inimiga
            for x in range(3, 12):
                for y in range(5, 10):
                    pygame.draw.rect(self.image, (100, 0, 0), 
                                    (x * self.pixel_size, y * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))
            
            # Asas da nave inimiga
            for x in range(5, 10):
                for y in range(2, 5):
                    pygame.draw.rect(self.image, (50, 50, 50), 
                                    (x * self.pixel_size, y * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))
                for y in range(10, 13):
                    pygame.draw.rect(self.image, (50, 50, 50), 
                                    (x * self.pixel_size, y * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH, WIDTH + 100)
        self.rect.y = random.randrange(50, HEIGHT - 100)
        self.speed = random.randrange(2, 5)
        
        # Movimento senoidal
        self.angle = random.randrange(0, 360)
        self.amplitude = random.randrange(10, 40)
        self.original_y = self.rect.y

    def update(self):
        self.rect.x -= self.speed
        # Movimento senoidal
        self.angle = (self.angle + 2) % 360
        self.rect.y = self.original_y + int(math.sin(math.radians(self.angle)) * self.amplitude)
        
        # Se o inimigo sair da tela, reposicioná-lo
        if self.rect.right < 0:
            self.rect.x = random.randrange(WIDTH, WIDTH + 100)
            self.original_y = random.randrange(50, HEIGHT - 100)
            self.rect.y = self.original_y
            self.speed = random.randrange(2, 5)

# Classe dos obstáculos (rochas)
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pixel_size = 2
        self.size = random.randrange(20, 40)
        self.image = create_pixel_surface(self.size, self.size, self.pixel_size)
        
        # Desenhar a rocha em estilo pixel art
        center = self.size // 2
        radius = self.size // 2 - 1
        
        # Gerar uma forma irregular para a rocha
        points = []
        num_points = 12
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            r = radius * (0.8 + 0.2 * random.random())
            x = center + int(r * math.cos(angle))
            y = center + int(r * math.sin(angle))
            points.append((x, y))
        
        # Preencher a rocha
        for x in range(self.size):
            for y in range(self.size):
                # Distância do centro
                dx = x - center
                dy = y - center
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist < radius:
                    # Variação de cor baseada na posição
                    shade = 100 + int(50 * (x / self.size)) - int(30 * (y / self.size))
                    shade = max(50, min(shade, 150))
                    color = (shade, shade//2, 0)
                    
                    # Adicionar textura
                    if random.random() < 0.2:
                        color = (shade - 20, shade//2 - 10, 0)
                    
                    pygame.draw.rect(self.image, color, 
                                    (x * self.pixel_size, y * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))
        
        # Desenhar o contorno
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            pygame.draw.line(self.image, (50, 30, 0), 
                            (x1 * self.pixel_size, y1 * self.pixel_size),
                            (x2 * self.pixel_size, y2 * self.pixel_size), 2)
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH, WIDTH + 300)
        self.rect.y = random.randrange(-100, HEIGHT - self.size)
        self.speed = random.randrange(1, 3)
        self.rotation = 0
        self.rotation_speed = random.choice([-1, 1]) * random.random() * 2

    def update(self):
        self.rect.x -= self.speed
        
        # Rotação simples (sem usar transform.rotate para manter o pixel art)
        # Na prática, para um jogo real, você usaria pygame.transform.rotate
        
        # Se a rocha sair da tela, reposicioná-la
        if self.rect.right < 0:
            self.rect.x = random.randrange(WIDTH, WIDTH + 300)
            self.rect.y = random.randrange(-100, HEIGHT - self.size)
            self.speed = random.randrange(1, 3)

# Classe para o fundo com paralaxe
class Background:
    def __init__(self):
        self.pixel_size = 2
        
        # Camada de água (fundo)
        self.water_layer = pygame.Surface((WIDTH, HEIGHT))
        self.water_layer.fill(WATER_BLUE)
        
        # Adicionar textura à água
        for _ in range(1000):
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            size = random.randrange(1, 3)
            shade = random.randrange(-20, 20)
            color = (
                max(0, min(255, WATER_BLUE[0] + shade)),
                max(0, min(255, WATER_BLUE[1] + shade)),
                max(0, min(255, WATER_BLUE[2] + shade))
            )
            pygame.draw.rect(self.water_layer, color, (x, y, size, size))
        
        # Camada de nuvens (meio)
        self.cloud_layer = pygame.Surface((WIDTH * 2, HEIGHT), pygame.SRCALPHA)
        self.cloud_layer.fill((0, 0, 0, 0))
        
        for _ in range(20):
            cloud_x = random.randrange(0, WIDTH * 2)
            cloud_y = random.randrange(0, HEIGHT // 2)
            cloud_size = random.randrange(50, 150)
            self.draw_cloud(self.cloud_layer, cloud_x, cloud_y, cloud_size)
        
        # Posições para o efeito de paralaxe
        self.cloud_pos = 0
        self.cloud_speed = 0.5
    
    def draw_cloud(self, surface, x, y, size):
        # Desenhar uma nuvem em estilo pixel art
        for i in range(5):
            cloud_x = x + random.randrange(-size//2, size//2)
            cloud_y = y + random.randrange(-size//4, size//4)
            cloud_radius = random.randrange(size//4, size//2)
            
            for px in range(cloud_x - cloud_radius, cloud_x + cloud_radius):
                for py in range(cloud_y - cloud_radius, cloud_y + cloud_radius):
                    if (px - cloud_x)**2 + (py - cloud_y)**2 <= cloud_radius**2:
                        alpha = random.randrange(30, 60)
                        pygame.draw.rect(surface, (255, 255, 255, alpha), (px, py, 2, 2))
    
    def update(self):
        # Atualizar posições para o efeito de paralaxe
        self.cloud_pos -= self.cloud_speed
        if self.cloud_pos <= -WIDTH:
            self.cloud_pos = 0
    
    def draw(self, surface):
        # Desenhar as camadas
        surface.blit(self.water_layer, (0, 0))
        surface.blit(self.cloud_layer, (self.cloud_pos, 0))
        surface.blit(self.cloud_layer, (self.cloud_pos + WIDTH, 0))

# Classe para explosões
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.pixel_size = 2
        self.size = size
        self.image = create_pixel_surface(size, size, self.pixel_size)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.draw_explosion_frame()
    
    def draw_explosion_frame(self):
        # Limpar a imagem
        self.image.fill(BLACK)
        
        # Desenhar a explosão em estilo pixel art
        center = self.size // 2
        max_radius = self.frame * 2
        
        if self.frame < 5:  # Expansão
            # Círculo central
            for x in range(self.size):
                for y in range(self.size):
                    dx = x - center
                    dy = y - center
                    dist = math.sqrt(dx*dx + dy*dy)
                    
                    if dist < max_radius:
                        if dist > max_radius - 2:
                            color = ORANGE
                        else:
                            color = (255, 255, 200)
                        
                        pygame.draw.rect(self.image, color, 
                                        (x * self.pixel_size, y * self.pixel_size, 
                                         self.pixel_size, self.pixel_size))
            
            # Partículas
            for _ in range(self.frame * 5):
                angle = random.random() * 2 * math.pi
                distance = random.random() * max_radius
                px = center + int(math.cos(angle) * distance)
                py = center + int(math.sin(angle) * distance)
                
                if 0 <= px < self.size and 0 <= py < self.size:
                    color = random.choice([ORANGE, (255, 255, 200), RED])
                    pygame.draw.rect(self.image, color, 
                                    (px * self.pixel_size, py * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))
        
        else:  # Dissipação
            fade = 255 - (self.frame - 5) * 30
            fade = max(0, fade)
            
            # Partículas esparsas
            for _ in range((10 - self.frame) * 10):
                angle = random.random() * 2 * math.pi
                distance = random.random() * max_radius
                px = center + int(math.cos(angle) * distance)
                py = center + int(math.sin(angle) * distance)
                
                if 0 <= px < self.size and 0 <= py < self.size:
                    color = (min(255, fade + random.randrange(0, 50)), 
                             min(255, fade//2 + random.randrange(0, 30)), 
                             0)
                    pygame.draw.rect(self.image, color, 
                                    (px * self.pixel_size, py * self.pixel_size, 
                                     self.pixel_size, self.pixel_size))
        
        self.image.set_colorkey(BLACK)
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame > 10:
                self.kill()
            else:
                self.draw_explosion_frame()

# Criar grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
rocks = pygame.sprite.Group()

# Criar o jogador
player = Player()
all_sprites.add(player)

# Criar inimigos
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Criar rochas
for i in range(5):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# Criar o fundo
background = Background()

# Configurações do jogo
game_clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

# Loop principal do jogo
running = True
game_over = False

while running:
    # Manter o jogo rodando na velocidade certa
    game_clock.tick(60)
    
    # Processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Controles do teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            if event.key == pygame.K_RIGHT:
                player.speed_x = 5
            if event.key == pygame.K_UP:
                player.speed_y = -5
            if event.key == pygame.K_DOWN:
                player.speed_y = 5
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_r and game_over:
                # Reiniciar o jogo
                game_over = False
                player.health = 100
                score = 0
                # Reposicionar o jogador
                player.rect.centerx = WIDTH // 4
                player.rect.bottom = HEIGHT - 50
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.speed_x < 0:
                player.speed_x = 0
            if event.key == pygame.K_RIGHT and player.speed_x > 0:
                player.speed_x = 0
            if event.key == pygame.K_UP and player.speed_y < 0:
                player.speed_y = 0
            if event.key == pygame.K_DOWN and player.speed_y > 0:
                player.speed_y = 0
    
    if not game_over:
        # Atualizar o fundo
        background.update()
        
        # Atualizar todos os sprites
        all_sprites.update()
        
        # Verificar colisões entre projéteis e inimigos
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 10
            # Criar uma explosão
            explosion = Explosion(hit.rect.center, 20)
            all_sprites.add(explosion)
            # Criar um novo inimigo
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        
        # Verificar colisões entre jogador e inimigos
        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            player.health -= 20
            # Criar uma explosão
            explosion = Explosion(hit.rect.center, 30)
            all_sprites.add(explosion)
            if player.health <= 0:
                game_over = True
                # Explosão final do jogador
                explosion = Explosion(player.rect.center, 40)
                all_sprites.add(explosion)
            # Criar um novo inimigo
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        
        # Verificar colisões entre jogador e rochas
        hits = pygame.sprite.spritecollide(player, rocks, False)
        for hit in hits:
            player.health -= 1
            if player.health <= 0:
                game_over = True
                # Explosão final do jogador
                explosion = Explosion(player.rect.center, 40)
                all_sprites.add(explosion)
        
        # Verificar colisões entre projéteis e rochas
        hits = pygame.sprite.groupcollide(bullets, rocks, True, False)
        for bullet, rock_list in hits.items():
            # Pequena explosão
            explosion = Explosion(bullet.rect.center, 10)
            all_sprites.add(explosion)
        
        # Atirar automaticamente
        if pygame.time.get_ticks() % 500 < 20:
            player.shoot()
    
    # Renderizar
    # Desenhar o fundo
    background.draw(screen)
    
    # Desenhar todos os sprites
    all_sprites.draw(screen)
    
    # Desenhar a pontuação
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Desenhar a barra de vida
    pygame.draw.rect(screen, (50, 50, 50), (10, 50, 102, 22))
    pygame.draw.rect(screen, RED, (11, 51, player.health, 20))
    
    # Mostrar tela de game over
    if game_over:
        go_text = font.render("GAME OVER - Pressione R para reiniciar", True, WHITE)
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2))
    
    # Atualizar a tela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
sys.exit()
