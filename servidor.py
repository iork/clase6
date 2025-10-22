from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel

from typing import List, Optional, Dict, Any

class Product(BaseModel):
	Id: int
	nombre: str
	categoria: str
	precio: float
	enStock: bool

class Product_out(BaseModel):
	nombre: str
	categoria: str
	precio: float
	enStock: bool

app=FastAPI(title="mi primer CRUD")
#PRODUCT_DB:List[Product]=[]
PRODUCT_DB:List[Dict[str, Any]] = [
    {"Id": 1, "nombre": "Laptop", "categoria": "electronica", "precio": 1200.50, "enStock": True},
    {"Id": 2, "nombre": "Smartphone", "categoria": "electronica", "precio": 499.99, "enStock": True},
    {"Id": 3, "nombre": "Vuelta al mundo", "categoria": "libros", "precio": 35.00, "enStock": True},
    {"Id": 4, "nombre": "Silla", "categoria": "muebles", "precio": 150.75, "enStock": True},
    {"Id": 5, "nombre": "Mouse", "categoria": "electronica", "precio": 25.99, "enStock": True},
    {"Id": 6, "nombre": "Mesa", "categoria": "muebles", "precio": 99.00, "enStock": True},
]

@app.post("/producto")
def add_update(prod: Product, response_model=Product_out):
    existe = False
    for i in range(len(PRODUCT_DB)):
        if PRODUCT_DB[i]["Id"] == prod.Id:
            existe = True
            break
    if existe == False:
        PRODUCT_DB.append(prod.model_dump())
        raise HTTPException(status_code= status.HTTP_201_CREATED, detail="Item creado")
        #return prod
    else:
    	raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item ya existe")

@app.get("/buscar")
def busca(producto_id: int):
    existe = False
    for i in range(len(PRODUCT_DB)):
        if PRODUCT_DB[i]["Id"] == producto_id:
            existe = True
            break
    if existe == False:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Producto No Encontrado")
        #return prod
    else:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="OK. Producto Encontrado")


@app.get("/borrar")
def borrar(producto_id: int):
    existe = False
    for i in range(len(PRODUCT_DB)):
        if PRODUCT_DB[i]["Id"] == producto_id:
            existe = True
            break
    if existe == False:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Producto No Encontrado")
        #return prod
    else:
        del PRODUCT_DB[i]
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Producto Eliminado")


@app.get("/productos/filtro")
def productos_filtro(
    categoria: Optional[str] = Query(None, description="Categoría a filtrar"),
    precio_max: Optional[float] = Query(None, description="Precio máximo permitido")
    ):
    productos_filtrados = PRODUCT_DB
    if categoria is not None:
        categoria_lower = categoria.lower() #pasarlo a minusculas para no caer en mas
        productos_filtrados = [
            p for p in productos_filtrados 
            if p["categoria"].lower() == categoria_lower
        ]
    if precio_max is not None:
        productos_filtrados = [
            p for p in productos_filtrados 
            if p["precio"] <= precio_max
        ]
    return productos_filtrados        
        
          
    