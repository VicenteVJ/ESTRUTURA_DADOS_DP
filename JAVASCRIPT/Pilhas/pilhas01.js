class Stack {//(Stack) = Pilha
    constructor() {
        this.items = []
    }

    
    push(element) {// Adiciona um elemento ao topo (push)
        this.items.push(element)
    }

    
    pop() {// Remove e retorna o elemento do topo (pop)
        if (this.isEmpty()) {
            return "A pilha está vazia"
        }
        return this.items.pop()
    }

    
    peek() {// Consulta o elemento no topo sem removê-lo (peek)
        if (this.isEmpty()) {
            return "A pilha está vazia"
        }
        return this.items[this.items.length - 1]
    }

    
    isEmpty() {// Verifica se a pilha está vazia
        return this.items.length === 0
    }

    
    printStack() {// Exibe a pilha como string
        return this.items.join(" -> ")
    }
}


const stack = new Stack()// Exemplo de uso

// Adicionando elementos
stack.push(10)
stack.push(20)
stack.push(30)
console.log("Pilha:", stack.printStack()) // Pilha: 10 -> 20 -> 30

// Removendo elemento da estrura pilha
console.log("Elemento removido:", stack.pop()) // Elemento removido: 30
console.log("Pilha após pop:", stack.printStack()) // Pilha: 10 -> 20

// Consultando o elemento do topo
console.log("Topo da pilha:", stack.peek()) // Topo da pilha: 20

// Verificando se a pilha está vazia
console.log("A pilha está vazia?", stack.isEmpty()) // A pilha está vazia? false
