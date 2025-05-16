class Grafo {
  constructor(numVertices) {
    this.numVertices = numVertices;
    this.matriz = new Array(numVertices).fill(0).map(() => new Array(numVertices).fill(0));
  }

  // Adicione uma aresta entre dois vértices
  addAresta(origem, destino) {
    if (origem >= 0 && origem < this.numVertices && destino >= 0 && destino < this.numVertices) {
      this.matriz[origem][destino] = 1;
    }
  }

  // Remova uma aresta entre dois vértices
  removeAresta(origem, destino) {
    if (origem >= 0 && origem < this.numVertices && destino >= 0 && destino < this.numVertices) {
      this.matriz[origem][destino] = 0;
    }
  }

  // Verifique se há uma aresta entre dois vértices
  hasAresta(origem, destino) {
    return this.matriz[origem][destino] === 1;
  }

  // Imprima a matriz do grafo
  printMatriz() {
    console.log(this.matriz.map(row => row.join(' ')).join('\n'));
  }
}

// Crie um grafo com 5 vértices
const grafo = new Grafo(5);

// Adicione arestas
grafo.addAresta(0, 1);
grafo.addAresta(1, 2);
grafo.addAresta(2, 3);
grafo.addAresta(3, 4);
grafo.addAresta(4, 0);

// Imprima a matriz do grafo
grafo.printMatriz();

// Verifique se há uma aresta entre os vértices 1 e 3
console.log(grafo.hasAresta(1, 3)); // true

// Remova uma aresta
grafo.removeAresta(1, 2);

// Imprima a matriz do grafo novamente
grafo.printMatriz();