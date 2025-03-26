
class Queue {// Classe que representa uma estrutura de fila (Queue)
    constructor() {
        this.items = [] // Array que armazenará os elementos da fila
    }

   
    enqueue(element) { // Método para inserir um elemento na fila (enqueue)
        this.items.push(element) // Adiciona o elemento ao final da fila
        console.log(`${element} foi adicionado à fila.`)
    }

    
    dequeue() {// Método para remover um elemento da fila (dequeue)
        if (this.isEmpty()) {
            console.log("A fila está vazia. Nada para remover.")
            return null; // Indica que não há elementos para remover
        }
        const removido = this.items.shift() // Remove o primeiro elemento da fila
        console.log(`${removido} foi removido da fila.`)
        return removido
    }

    
    peek() {// Método para visualizar o primeiro elemento da fila (peek)
        if (this.isEmpty()) {
            console.log("A fila está vazia. Não há elementos para exibir.")
            return null
        }
        console.log(`Primeiro elemento na fila: ${this.items[0]}`)
        return this.items[0] // Retorna o primeiro elemento da fila sem removê-lo
    }

    
    isEmpty() {// Método para verificar se a fila está vazia
        return this.items.length === 0
    }

   
    printQueue() { // Método para exibir todos os elementos da fila
        if (this.isEmpty()) {
            console.log("A fila está vazia.")
        } else {
            console.log(`Fila atual: [ ${this.items.join(' → ')} ]`)
        }
    }
}

// Exemplo de uso da fila
const fila = new Queue();

fila.enqueue(10)  // Adiciona 10
fila.enqueue(20)  // Adiciona 20
fila.enqueue(30)  // Adiciona 30
fila.printQueue() // Exibe: Fila atual: [ 10 → 20 → 30 ]

fila.dequeue()    // Remove o primeiro elemento (10)
fila.peek()        // Exibe: Primeiro elemento na fila: 20
fila.printQueue()  // Exibe: Fila atual: [ 20 → 30 ]
