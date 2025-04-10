/**
 * Implementa o algoritmo de ordenação Bubble Sort (ou ordenação por bolha).
 * Ordena uma lista comparando elementos adjacentes e os trocando de posição caso estejam fora de ordem.
 * O processo se repete até que a lista esteja ordenada.
 */


function bubbleSort(arr) {
  
  for (let i = 0; i < arr.length - 1; i++) {                 // Percorre a lista várias vezes

    for (let j = 0; j < arr.length - i - 1; j++) {     // Em cada passagem, compara pares de elementos adjacentes e a troca se estiverem na ordem errada
      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];      // Troca os elementos se estiverem na ordem errada
      }
    }
  }
  return arr;
}

let lista = [61, 34, 25, 12, 22, 11, 90];
console.log("Lista original:", lista);
console.log("Lista ordenada:", bubbleSort(lista));
