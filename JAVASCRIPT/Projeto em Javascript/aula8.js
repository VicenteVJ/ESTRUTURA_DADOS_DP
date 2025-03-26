const listaDeEstados = new Array(
    `São Paulo`,
    `Paraná`,
    `Rio de Janeiro`,
    `Rio Grande do sul`

    )
    
const idadeComprardor = 17
console.log("Destinos possiveis")
console.log(listaDeEstados)

if(idadeComprardor >= 18){//Se o comprador for maior de idade, executar esse comando
  console.log("Comprador maior de idade")
  listaDeEstados.splice(1,1)// remover item da lista
}else{//Senao execute esse comando aqui
console.log("Não é maior de idade e não posso vender")

}
console.log(listaDeEstados)
