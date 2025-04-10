// Classe que representa um nó da árvore
class No {
    constructor(valor) {
      this.valor = valor;
      this.esquerdo = null;
      this.direito = null;
    }
  }
  
  // Classe que representa a Árvore Binária
  class ArvoreBinaria {
    constructor() {
      this.raiz = null;
    }
  
    // Insere valores de forma manual (sem ordenar)
    inserirManual(valor, lado = 'esquerdo') {
      const novo = new No(valor);
  
      if (!this.raiz) {
        this.raiz = novo;
      } else {
        if (lado === 'esquerdo') {
          this.raiz.esquerdo = novo;
        } else {
          this.raiz.direito = novo;
        }
      }
    }
  
    // Mostra os dados da raiz e seus filhos
    mostrar() {
      console.log('Raiz:', this.raiz.valor);
      if (this.raiz.esquerdo)
        console.log('Esquerda:', this.raiz.esquerdo.valor);
      if (this.raiz.direito)
        console.log('Direita:', this.raiz.direito.valor);
    }
  }
  
  // Exemplo de uso
  const arvore = new ArvoreBinaria();
  arvore.inserirManual(10); // raiz
  arvore.inserirManual(5, 'esquerdo');
  arvore.inserirManual(15, 'direito');
  arvore.mostrar();
  