/**
 * Implementa o algoritmo de ordenação Selection Sort.
 * Ordena uma lista repetidamente encontrando o menor elemento da parte não ordenada e movendo-o para a posição correta.
 */



function selectionSort(arr) {
  
  for (let i = 0; i < arr.length - 1; i++) {     // Percorre a lista e encontra o menor elemento
    let menor = i;                              // Inicializa o índice do menor elemento como o primeiro elemento da parte não ordenada
    for (let j = i + 1; j < arr.length; j++) {  // Percorre a parte não ordenada para encontrar o menor elemento
      if (arr[j] < arr[menor]) {
        menor = j;                    // Atualiza o índice do menor elemento se encontrar um elemento menor
      }
    }
    [arr[i], arr[menor]] = [arr[menor], arr[i]];    // Troca o menor elemento com o primeiro elemento da parte não ordenada
  }
  return arr;
}


let lista = [61, 34, 25, 12, 22, 11, 90];
console.log("Lista original:", lista);
console.log("Lista ordenada:", selectionSort(lista));