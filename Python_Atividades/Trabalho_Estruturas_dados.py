# 1 – Faça um programa que mostre a mensagem: Sou Analista de Sistemas!
print("Sou Analista de Sistemas!")

# 2 – Faça um programa que peça dois números e imprima a soma.
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))
soma = num1 + num2
print(f"A soma de {num1} + {num2} = {soma}")

# 3 – Faça um programa que calcule a área de um quadrado, em seguida mostre o dobro desta área.
lado = float(input("Digite o lado do quadrado: "))
area = lado ** 2
dobro_area = area * 2
print(f"A área do quadrado é: {area}")
print(f"O dobro da área é: {dobro_area}")

# 4 - Faça um Programa que pergunte quanto você ganha por hora e o número de horas trabalhadas no mês. 
# Calcule e mostre o total do seu salário no referido mês.
valor_hora = float(input("Quanto você ganha por hora? "))
horas_trabalhadas = float(input("Quantas horas você trabalhou no mês? "))
salario = valor_hora * horas_trabalhadas
print(f"Seu salário no mês é: R$ {salario:.2f}")

# 5 – Faça um programa que converta metros em centímetros.
metros = float(input("Digite o valor em metros: "))
centimetros = metros * 100
print(f"{metros} metros equivalem a {centimetros} centímetros")

# 6 - Faça um Programa que peça dois números e imprima o maior deles.
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))

if num1 > num2:
    print(f"O maior número é: {num1}")
elif num2 > num1:
    print(f"O maior número é: {num2}")
else:
    print("Os números são iguais")


# 7 - Faça um Programa que verifique se uma letra digitada é "F" ou "M". 
# Conforme a letra escrever: F - Feminino, M – Masculino.
letra = input("Digite F ou M: ").upper()

if letra == "F":
    print("F - Feminino")
elif letra == "M":
    print("M - Masculino")
else:
    print("Letra inválida")


# 8 - Faça um Programa que leia três números e mostre-os em ordem decrescente.
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))
num3 = float(input("Digite o terceiro número: "))

# Criando uma lista e ordenando em ordem decrescente
numeros = [num1, num2, num3]
numeros.sort(reverse=True)

print("Números em ordem decrescente:")
for numero in numeros:
    print(numero)

# 9 - Faça um Programa que leia três números e mostre-os em ordem crescente.
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))
num3 = float(input("Digite o terceiro número: "))

# Criando uma lista e ordenando em ordem crescente
numeros = [num1, num2, num3]
numeros.sort()

print("Números em ordem crescente:")
for numero in numeros:
    print(numero)

# 10 - Faça um programa que pergunte o preço de três produtos e informe qual produto você deve comprar, 
# sabendo que a decisão é sempre pelo mais barato.
preco1 = float(input("Digite o preço do primeiro produto: R$ "))
preco2 = float(input("Digite o preço do segundo produto: R$ "))
preco3 = float(input("Digite o preço do terceiro produto: R$ "))

if preco1 < preco2 and preco1 < preco3:
    print(f"Você deve comprar o primeiro produto (R$ {preco1:.2f})")
elif preco2 < preco1 and preco2 < preco3:
    print(f"Você deve comprar o segundo produto (R$ {preco2:.2f})")
elif preco3 < preco1 and preco3 < preco2:
    print(f"Você deve comprar o terceiro produto (R$ {preco3:.2f})")
elif preco1 == preco2 and preco1 < preco3:
    print(f"Você pode comprar o primeiro ou o segundo produto (R$ {preco1:.2f})")
elif preco1 == preco3 and preco1 < preco2:
    print(f"Você pode comprar o primeiro ou o terceiro produto (R$ {preco1:.2f})")
elif preco2 == preco3 and preco2 < preco1:
    print(f"Você pode comprar o segundo ou o terceiro produto (R$ {preco2:.2f})")
else:
    print(f"Todos os produtos têm o mesmo preço (R$ {preco1:.2f})")