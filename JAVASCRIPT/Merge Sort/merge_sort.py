def merge_sort(lista, nivel=0);
    print(" " * nivel + "Dividindo:", lista)
    if len(lista) <= 1:
      return lista
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio], nivel + 1)
    direita = merge_sort(lista[meio:], nivel + 1)
    
    resultado = merge_sort(esquerda, nivel + 1) 
    print(" " * nivel + f"Resultado após merge: {resultado}")
    return resultado

def merge(esquerda, direita, nivel):
   resultado = []
   i = j = 0

   while i < len(esquerda) and j < len(direita):
      if esquerda[i] < direita[j]:
         resultado.append(esquerda[i])
         i += 1
      else:
         resultado.append(direita[j])
         j += 1
  
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])

        print(" " * nivel + f"Merging: {esquerda} + {direita} = {resultado}")
        return resultado
   
   #exemplo
   lista = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
   print("lista original:", lista_exemplo)

   lista_ordenada = merge_sort(lista_exemplo)
   print("\n lista ordenada:", lista_ordenada)