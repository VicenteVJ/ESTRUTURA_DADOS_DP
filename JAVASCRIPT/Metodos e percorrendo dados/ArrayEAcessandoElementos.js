let frutas = ["maçã", "banana", "laranja"]//Declarando três elementos dentro de um vetor
let numeros = new Array(10, 20, 30)// Array com três posições
let vazio = new Array(3) // Array com 3 posições vazias
console.log(frutas[0])  //Apresentando um valor que estiver dentro do indice zero
console.log(frutas[1])  
console.log(frutas[2])  

frutas[1] = "uva"// Irá substituir "banana" por "uva"
console.log(frutas)
frutas.push("abacaxi")//Vai inserir um valor
console.log(frutas) 
frutas.pop()//Irá remover o  ultimo item da lista
console.log(frutas)  
frutas.unshift("morango")//Insere um item no começo da lista
console.log(frutas) 
frutas.shift()//Remove um item do inicio da lista
console.log(frutas) 
frutas.splice(1, 1)// Remove 1 elemento a partir do índice 1
console.log(frutas) 


let citrus = frutas.slice(1, 3) //Copia uma parte do array
console.log(citrus)  
console.log(frutas.indexOf("laranja"))  //IndexOf, Encontra a posição dois (2)
console.log(frutas.indexOf("kiwi"))     //IndexOf  (não encontrado nenhum elemento), então 
//a posição é -1

