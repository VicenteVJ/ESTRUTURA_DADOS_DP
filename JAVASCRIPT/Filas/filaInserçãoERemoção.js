// Classe Queue para implementar a estrutura de fila
class Queue {
    constructor() {
        // Array para armazenar os elementos da fila
        this.items = [];
    }

    // Método para inserir um elemento na fila (enqueue)
    enqueue(element) {
        this.items.push(element);  // Adiciona o elemento no final da fila
        console.log(`Inserido: ${element}`);
    }

    // Método para remover um elemento da fila (dequeue)
    dequeue() {
        if (this.isEmpty()) {
            console.log("Fila vazia! Nada para remover.");
            return;
        }
        const removed = this.items.shift();  // Remove o primeiro elemento da fila
        console.log(`Removido: ${removed}`);
    }

    // Método para exibir o primeiro elemento da fila (peek)
    front() {
        if (this.isEmpty()) {
            console.log("Fila vazia!");
            return;
        }
        console.log(`Primeiro da fila: ${this.items[0]}`);
    }

    // Método que verifica se a fila está vazia
    isEmpty() {
        return this.items.length === 0;
    }

    // Método para exibir todos os elementos da fila
    display() {
        if (this.isEmpty()) {
            console.log("Fila vazia!");
        } else {
            console.log(`Fila: ${this.items.join(" → ")}`); // Exibe elementos separados por '→'
        }
    }
}

// --- Teste da implementação ---

// Cria uma nova instância da classe Queue
const fila = new Queue();

// Inserindo elementos na fila
fila.enqueue(10);  // Inserido: 10
fila.enqueue(20);  // Inserido: 20
fila.enqueue(30);  // Inserido: 30
fila.display();    // Fila: 10 → 20 → 30

// Removendo elementos da fila
fila.dequeue();    // Removido: 10
fila.display();    // Fila: 20 → 30

// Adicionando mais elementos
fila.enqueue(40);  // Inserido: 40
fila.display();    // Fila: 20 → 30 → 40

// Mostrando o primeiro elemento da fila
fila.front();      // Primeiro da fila: 20

// Removendo os elementos restantes
fila.dequeue();    // Removido: 20
fila.dequeue();    // Removido: 30
fila.dequeue();    // Removido: 40
fila.dequeue();    // Fila vazia! Nada para remover.
