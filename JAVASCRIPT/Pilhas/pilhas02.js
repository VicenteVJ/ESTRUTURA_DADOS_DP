function Stack() {
    let items = [] // Array privado que armazena os elementos

    
    this.push = function(element) {// Adiciona um elemento ao topo da pilha
        items.push(element)
    }

    
    this.pop = function() {// Remove e retorna o elemento do topo
        return items.length > 0 ? items.pop() : "A pilha está vazia";
    }

    
    this.peek = function() {// Retorna o elemento do topo sem removê-lo
        return items.length > 0 ? items[items.length - 1] : "A pilha está vazia";
    };

    
    this.isEmpty = function() {// Verifica se a pilha está vazia
        return items.length === 0
    }

    
    this.size = function() {// Retorna o tamanho da pilha
        return items.length;
    }

    
    this.print = function() {// Exibe a pilha no console
        console.log(items.join(" -> "));
    }
}


const stack = new Stack()//Estrutura pilha recebendo novos valores em uma String.

stack.push("A");
stack.push("B");
stack.push("C");

console.log("Elemento no topo:", stack.peek()); // C
stack.print(); // A -> B -> C

console.log("Elemento removido:", stack.pop()); // C
stack.print(); // A -> B

console.log("A pilha está vazia?", stack.isEmpty()); // false
console.log("Tamanho da pilha:", stack.size()); // 2
