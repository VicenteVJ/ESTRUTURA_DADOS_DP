class Node {//Criando a classe Node
    constructor(value) {//Construtor de lita ligadas
        this.value = value// Dado armazenado no nó
        this.next = null // Referência para o próximo nó
    }
}
class LinkedList {//Classe de manipulação de elementos
    constructor() {
        this.head = null  // Cabeça da lista (primeiro elemento)
        this.size = 0     // Contador de elementos
    }

    // Adiciona um elemento no final da lista
    append(value) {
        const newNode = new Node(value)

        if (!this.head) {
            this.head = newNode  // Se a lista estiver vazia
        } else {
            let current = this.head//inicializando a variável current
            while (current.next) {//Enquanto a lista percorre até o ultimo elemento
                //que seja encontrado. 
                current = current.next//passa de variável até a proxima variavel
            }
            current.next = newNode//encontrando o proxímo nó
        }

        this.size++//irá imcrementar mais um numero a lista
    }

    
    print() {// Exibe os elementos da lista
        let current = this.head//começa pelo primeiro nó
        let result = ""//Uma string que armazena a saída formatada
        while (current) {//Enquanto houver um nó valído ele irá percorrer a lista
            result += `${current.value} -> `//irá adicionar um valor na lista
            current = current.next//Ele irá avançar para o proximo nó
        }
        console.log(result + "null")//Exibe a string resultado
    }

    
    remove(value) {// Remove um elemento pelo valor
        if (!this.head) return // Retorna uma lista vazia

        if (this.head.value === value) {//Se o valor do primeiro nó for igual ao valor passado
            //para a função, então o primeiro nó a ser removido é o primeiro da lista.
            this.head = this.head.next//O ponteiro é atualizado para o proximo nó, e removendo
            //o primeiro nó da lista.
            this.size--//Aqui ele irá fazer um decremento ou seja, retirar um valor(Diminuir) 
            return
        }

        let current = this.head//Ele permite que você percorra ou manipule a lista
        //  sem perder a referência ao primeiro elemento (head).
        let previous = null//inicializando a variavel (previous), como null

        while (current && current.value !== value) {//Enquanto ele percorre toda a lista e a
            //variável não for null, ele irá evitar erro caso o fim da lista seja alcançado
            previous = current
            current = current.next
        }

        if (current) {//Se current não for null, significa que o 
        // valor procurado foi encontrado na lista.
            previous.next = current.next
            this.size--
        }
    }

    // Busca um elemento na lista
    search(value) {//Irá procurar um valor especifico
        let current = this.head//Começa pelo primeiro no na lsta

        while (current) {//Enquanto houver um no na lista
            if (current.value === value) {//Se o valor do nó atual for o valor procurado
                return true//Retorna `true` porque o valor foi encontrado
            }
            current = current.next
        }

        return false
    }
}
const lista = new LinkedList() //cria uma lista

lista.append(10)//Adiciona o valor 10 à lista, esse valor será o primeiro nó
lista.append(20)
lista.append(30)

lista.print()  // 10 -> 20 -> 30 -> null

lista.remove(20)
lista.print()  // 10 -> 30 -> null

console.log(lista.search(30)) // true
console.log(lista.search(50)) // false