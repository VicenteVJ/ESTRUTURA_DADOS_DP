class Node {
    constructor(value) {
        this.value = value;
        this.children = []
    }

    addChild(child) {
        this.children.push(child);
    }
}

class Tree {
    constructor(rootValue) {
        this.root = new Node(rootValue);
    }

    depthFirstSearch(node = this.root) {
        console.log(node.value)
        for (let child of node.children) {
            this.depthFirstSearch(child)
        }
    }

    breadthFirstSearch() {
        const queue = [this.root]

        while (queue.length) {
            const current = queue.shift()
            console.log(current.value)

            for (let child of current.children) {
                queue.push(child)
            }
        }
    }
}

// Exemplo de uso
const tree = new Tree('A') // Nó raiz
const node1 = new Node(1)
const nodeB = new Node('B')
const node2 = new Node(2)
const nodeC = new Node('C')
const node3 = new Node(3)
const nodeD = new Node('D')

// Estrutura da árvore
tree.root.addChild(node1) // Adiciona o nó 1 como filho do nó raiz
tree.root.addChild(nodeB)
tree.root.children[0].addChild(node2)
tree.root.children[0].addChild(nodeC)
tree.root.children[1].addChild(node3)
tree.root.children[1].addChild(nodeD)

console.log('Busca em profundidade (DFS):')
tree.depthFirstSearch() //saída esperada: A, 1, B, 2, C, 3, D

console.log('\nBusca em largura (BFS):')
tree.breadthFirstSearch() //saída esperada: A, 1, B, 2, C, 3, D