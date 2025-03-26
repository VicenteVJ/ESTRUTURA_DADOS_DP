console.log("Trabalhando com listas")

const listaDeEstados = new Array(
    `São Paulo`,
    `Paraná`,
    `Rio de Janeiro`,
    `Rio Grande do sul`

    )
    listaDeEstados.push(`Pernambuco`,)/*Push, irá adicionar um item a lista*/ 
    console.log("Estados")
    console.log(listaDeEstados)

    listaDeEstados.splice(3,1)//Splice, ele retira um elemento da lista
    console.log(listaDeEstados)