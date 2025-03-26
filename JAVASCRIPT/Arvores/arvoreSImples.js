class Node {
    constructor(value) {
        this.value = value;
        this.children = [];
    }

    addChild(value) {
        this.children.push(new Node(value));
    }
}

class Tree {
    constructor(rootValue) {
        this.root = new Node(rootValue); // Cria o nó raiz
    }

    depthFirstSearch(node = this.root) { // Método para percorrer a árvore em profundidade
        console.log(node.value); // Imprime o valor do nó
        for (let child of node.children) {
            this.depthFirstSearch(child); // Percorre a subárvore
        }
    }

    breadthFirstSearch(node = this.root) { // Método para percorrer a árvore em largura
        const queue = [node]; // Cria uma fila com o nó raiz

        while (queue.length) {
            const current = queue.shift(); // Remove o primeiro nó da fila
            console.log(current.value); // Visita o nó atual

            for (let child of current.children) {
                queue.push(child);
            }
        }
    }
}

// Exemplo de uso
const tree = new Tree('A'); // Nó raiz

// Estrutura da árvore
tree.root.addChild('B');
tree.root.addChild('C');
tree.root.children[0].addChild('D');
tree.root.children[0].addChild('E');
tree.root.children[1].addChild('F');

console.log('Busca em profundidade (DFS):');
tree.depthFirstSearch(); // Saída esperada: A, B, D, E, C, F

console.log('\nBusca em largura (BFS):');
tree.breadthFirstSearch(); // Saída esperada: A, B, C, D, E, F