class Grafo {
  constructor() {
    this.vertices = [];
    this.arestas = {};
  }

  adicionarVertice(valor) {
    this.vertices.push(valor);
    this.arestas[valor] = [];
  }

  adicionarAresta(origem, destino) {
    if (this.arestas[origem] && this.arestas[destino]) {
      this.arestas[origem].push(destino);
      this.arestas[destino].push(origem);
    }
  }

  imprimirGrafo() {
    for (let vertice of this.vertices) {
      console.log(`Vertice: ${vertice}`);
      console.log(`Arestas: ${this.arestas[vertice]}`);
    }
  }
}

// Criar um grafo
let grafo = new Grafo();

// Adicionar vértices
grafo.adicionarVertice(1);
grafo.adicionarVertice(2);
grafo.adicionarVertice(3);
grafo.adicionarVertice(4);
grafo.adicionarVertice(5);
grafo.adicionarVertice(6);

// Adicionar arestas
grafo.adicionarAresta(1, 2);
grafo.adicionarAresta(2, 3);
grafo.adicionarAresta(3, 4);
grafo.adicionarAresta(4, 5);
grafo.adicionarAresta(5, 6);
grafo.adicionarAresta(6, 1);

// Imprimir o grafo
grafo.imprimirGrafo();