# operadores lógicos
# and (e) or (ou) not (não)
# and - Todas as condições precisam ser verdadeiras
"""Se qualquer valor for considerado falso, a expressão inteira será avaliada naquele valor

São consideradas false (que você ja viu)

0.0.0  ('') - uma string vazia false

Existe o tipo (None) que é usado para representar um não valor.
"""

entrada = input('[E]ntrar [S]air:') #input está veririfcando a variavel [E] e a variavel [S]
senha_digitada = input('Senha:')#verificando a variavel senha

senha_permitida = '1357910'

if entrada == 'E' and senha_digitada == senha_permitida:#se a variavel senha for verdadeira(True), irá executar
    #as informações depois do operador(and).
    print('Entrar')

else: 
    print('Sair')    

"""print(True and False and True)
print(bool(''))""" 