import turtle
import random

# --- Configuração da janela ---
janela = turtle.Screen()
janela.title("Pega Quadrados!")
janela.bgcolor("lightblue")
janela.setup(width=600, height=600)

# --- Criação do jogador ---
jogador = turtle.Turtle()
jogador.shape("turtle")
jogador.color("green")
jogador.penup()
jogador.speed(0)

# --- Criação do alvo (quadrado) ---
alvo = turtle.Turtle()
alvo.shape("square")
alvo.color("red")
alvo.penup()
alvo.speed(0)
alvo.goto(random.randint(-280, 280), random.randint(-280, 280))

# --- Pontuação ---
pontuacao = 0
escreve = turtle.Turtle()
escreve.hideturtle()
escreve.penup()
escreve.goto(0, 260)
escreve.write(f"Pontos: {pontuacao}", align="center", font=("Arial", 16, "bold"))

# --- Funções de movimento ---
def cima():
    y = jogador.ycor()
    if y < 280:
        jogador.sety(y + 20)

def baixo():
    y = jogador.ycor()
    if y > -280:
        jogador.sety(y - 20)

def esquerda():
    x = jogador.xcor()
    if x > -280:
        jogador.setx(x - 20)

def direita():
    x = jogador.xcor()
    if x < 280:
        jogador.setx(x + 20)

# --- Teclas ---
janela.listen()
janela.onkeypress(cima, "Up")
janela.onkeypress(baixo, "Down")
janela.onkeypress(esquerda, "Left")
janela.onkeypress(direita, "Right")

# --- Função principal do jogo ---
def jogar():
    global pontuacao

    if jogador.distance(alvo) < 20:
        alvo.goto(random.randint(-280, 280), random.randint(-280, 280))
        pontuacao += 1
        escreve.clear()
        escreve.write(f"Pontos: {pontuacao}", align="center", font=("Arial", 16, "bold"))

    # Chama a função novamente após 50ms
    janela.ontimer(jogar, 50)

# Inicia o jogo
jogar()

# Mantém a janela aberta
janela.mainloop()
