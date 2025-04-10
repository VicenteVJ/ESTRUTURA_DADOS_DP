function notSorting(arr) {
    let len = arr.length;
    
    for (let i = 0; i < len - 1; i++) {
        // Percorre os elementos, mas não faz trocas
        console.log(`Comparando ${arr[i]} e ${arr[i + 1]}`);
    }

    return arr; // Retorna o array sem alterações
}

// Exemplo de uso
let numeros = [64, 34, 25, 12, 22, 11, 90];
console.log("Array original:", numeros);
console.log("Após a função:", notSorting(numeros));
