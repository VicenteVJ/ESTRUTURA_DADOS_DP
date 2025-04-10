function bubbleSort(arr) {
    let len = arr.length // Obtém o tamanho do array
    let swapped // Variável para verificar se houve trocas na iteração

    do {
        swapped = false // Reseta a variável a cada iteração
        for (let i = 0; i < len - 1; i++) {
            // Se o elemento atual for maior que o próximo, trocamos os dois
            if (arr[i] > arr[i + 1]) {
                ,
                // Troca os elementos usando desestruturação
                [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]]
                swapped = true // Marca que houve troca
            }
        }
        len-- // Reduz o tamanho da verificação, pois o maior já está na posição correta
    } while (swapped); // Repete enquanto houver trocas

    return arr // Retorna o array ordenado
}

// Exemplo de uso
let numeros = [64, 34, 25, 12, 22, 11, 90] // Array de exemplo
console.log("Array ordenado:", bubbleSort(numeros)) // Chama a função e exibe o resultado
