let numeros = [10, 20, 30, 40, 50]//altera a variavel

console.log(numeros[0]) //Acessando elementos apartir do indice zero

numeros[1] = 25; // Modificando valores de vinte para vinte e cinco
console.log(numeros)     

numeros.push(60);
console.log(numeros) // Adicionando elementos, mais um número


numeros.splice(2, 1)// Remove o elemento na posição 2
console.log(numeros)     