function bubbleSortNomes(arr) {//função bubbleSortnomes, recebe uma array arr como parâmetro.
    //Esse array conterá os nomes a serem ordenados.
    let len = arr.length;//Armazena o tamanho do array na variável (len), pois será usado no loop.
    let swapped;//Declara a variável (swapped), que indicará se houve trocas entre elementos na iteração.

    do {
        swapped = false;
        for (let i = 0; i < len - 1; i++) {//percorre o array até -1 (pois será comparada arr[i] com arr[i+1])
            // Comparação alfabética entre dois nomes
            if (arr[i].toLowerCase() > arr[i + 1].toLowerCase()) {//Compara os nomes convertidos para minúsculas 
            // (toLowerCase()) para evitar problemas com maiúsculas e minúsculas.
                // Troca os nomes de posição
                [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]];//Troca os elementos de posição usando
                //  desestruturação de array.
                swapped = true;
            }
        }
        len--; // Reduz o tamanho da verificação
    } while (swapped);//O loop continuará rodando enquanto houver trocas (swapped === true)

    return arr; // Retorna o array ordenado
}

// Exemplo de uso
let nomes = ["Carlos", "Ana", "Bruno", "Eduardo", "Diana"];
console.log("Nomes ordenados:", bubbleSortNomes(nomes));
