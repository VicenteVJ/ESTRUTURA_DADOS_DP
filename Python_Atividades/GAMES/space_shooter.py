import pygame
import random
import sys
import os

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Classe do jogador (nave)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Criar uma nave simples (retângulo colorido)
        self.image = pygame.Surface((50, 30))
        self.image.fill(WHITE)
        # Desenhar detalhes na nave
        pygame.draw.polygon(self.image, ORANGE, [(0, 15), (15, 0), (15, 30)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.bottom = HEIGHT - 20
        self.speed_x = 0
        self.speed_y = 0
        self.shoot_delay = 250  # Tempo entre tiros em milissegundos
        self.last_shot = pygame.time.get_ticks()
        self.health = 100

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
        self.image = pygame.Surface((10, 5))
        self.image.fill(ORANGE)
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
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH, WIDTH + 100)
        self.rect.y = random.randrange(50, HEIGHT - 100)
        self.speed = random.randrange(2, 6)

    def update(self):
        self.rect.x -= self.speed
        # Se o inimigo sair da tela, reposicioná-lo
        if self.rect.right < 0:
            self.rect.x = random.randrange(WIDTH, WIDTH + 100)
            self.rect.y = random.randrange(50, HEIGHT - 100)
            self.speed = random.randrange(2, 6)

# Classe dos obstáculos (rochas)
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = random.randrange(40, 100)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(BLUE)
        # Desenhar detalhes na rocha
        pygame.draw.circle(self.image, (100, 100, 100), (self.size//2, self.size//2), self.size//2)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH, WIDTH + 300)
        self.rect.y = random.randrange(-100, HEIGHT - self.size)
        self.speed = random.randrange(1, 3)

    def update(self):
        self.rect.x -= self.speed
        # Se a rocha sair da tela, reposicioná-la
        if self.rect.right < 0:
            self.rect.x = random.randrange(WIDTH, WIDTH + 300)
            self.rect.y = random.randrange(-100, HEIGHT - self.size)
            self.speed = random.randrange(1, 3)

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

# Configurações do jogo
clock = pygame.time.get_ticks()
score = 0
font = pygame.font.SysFont(None, 36)

# Loop principal do jogo
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    # Manter o jogo rodando na velocidade certa
    clock.tick(60)
    
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
                player.rect.bottom = HEIGHT - 20
                
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
        # Atualizar todos os sprites
        all_sprites.update()
        
        # Verificar colisões entre projéteis e inimigos
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 10
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        
        # Verificar colisões entre jogador e inimigos
        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            player.health -= 20
            if player.health <= 0:
                game_over = True
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        
        # Verificar colisões entre jogador e rochas
        hits = pygame.sprite.spritecollide(player, rocks, False)
        for hit in hits:
            player.health -= 1
            if player.health <= 0:
                game_over = True
        
        # Atirar automaticamente
        if pygame.time.get_ticks() % 500 < 20:
            player.shoot()
    
    # Renderizar
    # Fundo azul para simular água/céu como na imagem
    screen.fill((50, 100, 150))
    
    # Desenhar todos os sprites
    all_sprites.draw(screen)
    
    # Desenhar a pontuação
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Desenhar a barra de vida
    pygame.draw.rect(screen, RED, (10, 50, player.health, 20))
    pygame.draw.rect(screen, WHITE, (10, 50, 100, 20), 2)
    
    # Mostrar tela de game over
    if game_over:
        go_text = font.render("GAME OVER - Pressione R para reiniciar", True, WHITE)
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2))
    
    # Atualizar a tela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
sys.exit()
