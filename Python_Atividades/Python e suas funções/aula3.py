"""Python = linguagem de programação
Tipo de tipagem = Dinâmica / Forte = Dinâmica, saber que tipo de dado primitivo está sendo 
colocado.
ex. 1234 int, string- texto.
str -> string -> texto
Strings são textos que estão dentro de aspas -> """

#aspas simples
print('Daniel')  

#aspas duplas
print("Daniel Silva") #interpretador irá mostrar uma string

#escape
print("Pedro \"Silva\"") #O interpretador irá mostrar apenas o Pedro, 
#após isso, quando colocar (\""ele não irá interpretar)
#apenas irá mostrar as aspas e o texto que você colocar no dentro.
#  Isso se chama caracter de (escape).

#r
print(r"Pedro \"Silva\"") #quando colocamos o caraster de escape (r), 
#ele me da a opção de aparecer tudo que estiver
#dentro de uma string

print(1,'"Daniel "Silva"')