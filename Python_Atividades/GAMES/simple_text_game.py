import random
import time
import os

class SimpleSpaceShooter:
    def __init__(self):
        self.player_pos = 5
        self.score = 0
        self.health = 100
        self.enemies = []
        self.bullets = []
        self.game_width = 20
        self.game_height = 10
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def spawn_enemy(self):
        if random.random() < 0.3:  # 30% chance de spawnar inimigo
            enemy_pos = random.randint(0, self.game_height - 1)
            self.enemies.append([self.game_width - 1, enemy_pos])
    
    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy[0] -= 1
            if enemy[0] < 0:
                self.enemies.remove(enemy)
                self.health -= 10
    
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet[0] += 1
            if bullet[0] >= self.game_width:
                self.bullets.remove(bullet)
    
    def check_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet[0] == enemy[0] and bullet[1] == enemy[1]:
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break
    
    def shoot(self):
        self.bullets.append([1, self.player_pos])
    
    def draw_game(self):
        self.clear_screen()
        
        # Criar o campo de jogo
        field = [[' ' for _ in range(self.game_width)] for _ in range(self.game_height)]
        
        # Desenhar jogador
        field[self.player_pos][0] = '>'
        
        # Desenhar inimigos
        for enemy in self.enemies:
            if 0 <= enemy[1] < self.game_height and 0 <= enemy[0] < self.game_width:
                field[enemy[1]][enemy[0]] = 'X'
        
        # Desenhar projéteis
        for bullet in self.bullets:
            if 0 <= bullet[1] < self.game_height and 0 <= bullet[0] < self.game_width:
                field[bullet[1]][bullet[0]] = '-'
        
        # Imprimir o campo
        print("=" * (self.game_width + 2))
        for row in field:
            print("|" + "".join(row) + "|")
        print("=" * (self.game_width + 2))
        
        print(f"Pontuação: {self.score} | Vida: {self.health}")
        print("Controles: W/S (mover), SPACE (atirar), Q (sair)")
        print("Jogador: >  Inimigos: X  Projéteis: -")
    
    def get_input(self):
        # Simulação de input não-bloqueante (versão simplificada)
        try:
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                return key
        except ImportError:
            # Para sistemas Unix/Linux (versão simplificada)
            import select
            import sys
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                return sys.stdin.readline().strip().lower()
        return None
    
    def run(self):
        print("=== SPACE SHOOTER TEXTO ===")
        print("Pressione ENTER para começar...")
        input()
        
        while self.health > 0:
            self.draw_game()
            
            # Input do jogador (versão simplificada)
            print("Digite comando (w/s/space/q): ", end="")
            command = input().lower()
            
            if command == 'q':
                break
            elif command == 'w' and self.player_pos > 0:
                self.player_pos -= 1
            elif command == 's' and self.player_pos < self.game_height - 1:
                self.player_pos += 1
            elif command == 'space' or command == ' ':
                self.shoot()
            
            # Atualizar jogo
            self.spawn_enemy()
            self.update_enemies()
            self.update_bullets()
            self.check_collisions()
            
            time.sleep(0.1)
        
        self.clear_screen()
        print("=== GAME OVER ===")
        print(f"Pontuação Final: {self.score}")

# Executar o jogo
if __name__ == "__main__":
    game = SimpleSpaceShooter()
    game.run()
