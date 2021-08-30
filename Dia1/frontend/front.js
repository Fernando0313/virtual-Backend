const BASE_URL="http://127.0.0.1:8000"

const btnProductos =document.getElementById("btn-traer-productos");
const nombre_producto = document.getElementById("non_producto");
const precio_producto = document.getElementById("prec_producto");
const btnAgregar = document.getElementById("btn-agregar-producto");
fetch(BASE_URL+"/",{method:"GET"}).then((respuesta)=>{
    console.log(respuesta.status)
})

btnProductos.onclick=(e)=>{
    console.log("Me hizo click")
    fetch(BASE_URL+"/productos",{method:"GET"}).then((respuesta)=>{
        return respuesta.json()
        
    })
    .then((productos)=>{
        console.log(productos)
    })
}
// btnProductos.addEventListener("click",()=>{
//     console.log("Me hizo click")
// })
btnAgregar.onclick= async(e)=>{
    console.log(nombre_producto.value);
    console.log(precio_producto.value)
    const respuesta= await fetch(BASE_URL+"/productos",{
        method:"POST",
        body:JSON.stringify({
            nombre:nombre_producto.value,
            precio:precio_producto.value
        }),
        headers:{
            "Content-Type":"application/json"
        }
    })

    const rpta=await respuesta.json()

    console.log(rpta)
}