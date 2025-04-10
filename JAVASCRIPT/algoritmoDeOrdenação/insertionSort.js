/**
 * Implementa o algoritmo de ordenação Insertion Sort.
 * Ordena uma lista de maneira semelhante a como organizamos cartas em um jogo:
 * pegamos uma carta e a inserimos na posição correta em relação às anteriores.
 */


function insertionSort(arr) {
  
  for (let i = 1; i < arr.length; i++) {     // Assume que o primeiro elemento já está ordenado
    let elemento = arr[i];                  // Pega o próximo elemento
        let j = i - 1;                     // Inicializa o índice da posição correta para o elemento
    while (j >= 0 && arr[j] > elemento) {    // Compara o elemento com os anteriores e move-o para a posição correta
      arr[j + 1] = arr[j];                   // Move o elemento anterior para a posição seguinte
      j--;                           // Decrementa o índice para comparar com o próximo elemento anterior
    }
    
    arr[j + 1] = elemento;         
  }
  return arr;
}

let lista = [63, 34, 25, 12, 22, 11, 90];
console.log("Lista original:", lista);
console.log("Lista ordenada:", insertionSort(lista));