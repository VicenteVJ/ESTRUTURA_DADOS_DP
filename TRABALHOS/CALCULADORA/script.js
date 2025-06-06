// Estrutura de dados para as categorias de IMC
const categoriaIMC = [
    { min: 0, max: 18.49, classificacao: "Abaixo do peso", classe: "abaixo-peso" },
    { min: 18.5, max: 24.99, classificacao: "Peso normal", classe: "peso-normal" },
    { min: 25, max: 29.99, classificacao: "Sobrepeso", classe: "sobrepeso" },
    { min: 30, max: 34.99, classificacao: "Obesidade grau 1", classe: "obesidade-1" },
    { min: 35, max: 39.99, classificacao: "Obesidade grau 2", classe: "obesidade-2" },
    { min: 40, max: Infinity, classificacao: "Obesidade grau 3", classe: "obesidade-3" }
];

// Elementos do DOM
const pesoInput = document.getElementById('peso');
const alturaInput = document.getElementById('altura');
const calcularBtn = document.getElementById('calcular');
const resultadoDiv = document.getElementById('resultado');
const valorIMC = document.getElementById('valor-imc');
const classificacaoSpan = document.getElementById('classificacao');
const infoBar = document.getElementById('info-bar');

// Função para calcular o IMC
function calcularIMC(peso, altura) {
    return peso / (altura * altura);
}

// Função para obter a categoria com base no valor do IMC
function obterCategoriaIMC(imc) {
    return categoriaIMC.find(categoria => imc >= categoria.min && imc <= categoria.max);
}

// Função para formatar o número com 1 casa decimal
function formatarNumero(numero) {
    return numero.toFixed(1);
}

// Evento de clique no botão calcular
calcularBtn.addEventListener('click', () => {
    // Obter valores dos inputs
    const peso = parseFloat(pesoInput.value);
    const altura = parseFloat(alturaInput.value);
    
    // Validar inputs
    if (isNaN(peso) || isNaN(altura) || peso <= 0 || altura <= 0) {
        alert('Por favor, insira valores válidos para peso e altura.');
        return;
    }
    
    // Calcular IMC
    const imc = calcularIMC(peso, altura);
    
    // Obter categoria
    const categoria = obterCategoriaIMC(imc);
    
    // Exibir resultado
    valorIMC.textContent = formatarNumero(imc);
    classificacaoSpan.textContent = categoria.classificacao;
    
    // Definir cor da barra de informação
    infoBar.className = categoria.classe;
    
    // Mostrar resultado
    resultadoDiv.classList.remove('hidden');
});

// Permitir o uso da tecla Enter para calcular
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        calcularBtn.click();
    }
});

// Limpar campos ao carregar a página
window.addEventListener('load', () => {
    pesoInput.value = '';
    alturaInput.value = '';
    resultadoDiv.classList.add('hidden');
});