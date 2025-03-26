console.log("Trabalhando com atribuição de variaveis")

const idade = 30
let nome = "Pedro"/*Let é para mudar o nome da variavel declarada.*/
const sobreNome = "galhardo"


//console.log(nome + "" sobreNome)
console.log(idade)
console.log(nome, sobreNome)
console.log(`Meu nome é ${nome} ${sobreNome}`)

nome = nome + sobreNome
nome = "Daniel"//com a função(Let), consigo mudar meu nome.
console.log(nome)

/*Obs: O javascript é considerado uma linguagem de tipagem fraca
pois o mesmo deixa mudar o nome das minhas variáveis declaradas.
Um exemplo disso é o nosso (Let), ele serve para determinados momentos na programação
mas nunca para alterar uma variável declarada em execução.

(Tipagem Fraca)
Ex: Javascript, PHP, Perl, Lua.*/


/*Algumas linguagem de programação teria uma tipagem forte, pois ele não deixa que você mude
uma variável em execução.
(Tipagem Forte)
Ex: java, Python, C#, Rust, Kotlin, */


