class Node {
  // Classe que representa um nó da árvore
  constructor(value) {
    this.value = value;
    this.left = null;
    this.right = null;
  }
}

class BinarySearchTree {
  // Classe que representa uma árvore binária de busca
  constructor() {
    this.root = null;
  }

  insert(value) {
    // Método para inserir um nó na árvore
    const newNode = new Node(value);
    if (!this.root) {
      this.root = newNode;
    } else {
      this._insertNode(this.root, newNode);
    }
  }

  _insertNode(Node, newNode) {
    // Método privado para inserção recursiva (não é um método público)
    if (newNode.value < Node.value) {
      if (!Node.left) {
        Node.left = newNode;
      } else {
        this._insertNode(Node.left, newNode);
      }
    } else {
      if (!Node.right) {
        Node.right = newNode; // Se não houver filho na direita, insira o novo nó
      } else {
        this._insertNode(Node.right, newNode); // Se houver filho na direita, insira o novo nó
      }
    }
  }

  inOrder(Node = this.root) {
    // Método para percorrer a árvore em ordem
    if (Node) {
      this.inOrder(Node.left); // Percorre a subárvore esquerda (In-order traversal) -> esquerda, raiz, direita
      console.log(Node.value); // Imprime o valor do nó
      this.inOrder(Node.right); // Percorre a subárvore direita
    }
  }

  preOrder(Node = this.root) {
    // Método para percorrer a árvore em pre-ordem (Pre-order traversal) -> raiz, esquerda, direita
    if (Node) {
      console.log(Node.value); // Imprime o valor do nó
      this.preOrder(Node.left); // Percorre a subárvore esquerda
      this.preOrder(Node.right); // Percorre a subárvore direita
    }
  }

  postOrder(Node = this.root) {
    // Método para percorrer a árvore em post-ordem (Post-order traversal) -> esquerda, direita, raiz
    if (Node) {
      this.postOrder(Node.left); // Percorre a subárvore esquerda
      this.postOrder(Node.right); // Percorre a subárvore direita
      console.log(Node.value); // Imprime o valor do nó
    }
  }
}