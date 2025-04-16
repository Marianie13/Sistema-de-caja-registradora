from productos import obtener_productos

def buscar_producto(nombre):
    productos = obtener_productos()
    for p in productos:
        if p["nombre"] == nombre:
            return p
    return None

def agregar_al_carrito(carrito, nombre_producto, cantidad):
    producto = buscar_producto(nombre_producto)
    if not producto:
        raise ValueError("Producto no encontrado.")

    if cantidad > producto["stock"]:
        raise ValueError("Stock insuficiente para este producto.")

    producto["stock"] -= cantidad
    carrito.append({
        "nombre": producto["nombre"],
        "precio": producto["precio"],
        "cantidad": cantidad
    })

def calcular_total(carrito):
    return sum(item["precio"] * item["cantidad"] for item in carrito)

def guardar_historial(carrito):
    with open("historial.txt", "a") as archivo:
        for item in carrito:
            total = item["precio"] * item["cantidad"]
            archivo.write(f"{item['nombre']}, {item['cantidad']}, {total}\n")