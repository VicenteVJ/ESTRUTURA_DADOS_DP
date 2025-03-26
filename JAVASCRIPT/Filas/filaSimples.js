
let fila = []// Criação da fila usando array


function inserir(elemento) {// Função para inserir na fila
    fila.push(elemento) // Adiciona ao final da fila
    console.log(`Inserido: ${elemento}`);//inserindo na variavel elemento
    exibirFila()
}


function remover() {// Função para remover da fila
    if (fila.length === 0) {//irá retomar o numero de elementos dentro da fila(array).

        console.log("Fila vazia! Nada para remover.");
        return;
    }
    const removido = fila.shift(); // Remove o primeiro elemento
    console.log(`Removido: ${removido}`);
    exibirFila();
}

// Função para exibir os elementos da fila
function exibirFila() {
    console.log(`Fila atual: [ ${fila.join(' → ')} ]`);
}

// Teste das funções
inserir(1);
inserir(2);
inserir(3);
remover();   // Remove o primeiro elemento (1)
inserir(4);
exibirFila(); // Fila atual: [ 2 → 3 → 4 ]
remover();
remover();
remover();    // Agora a fila estará vazia
