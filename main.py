import tkinter as tk
from tkinter import ttk, messagebox
from productos import obtener_productos
from operaciones import agregar_al_carrito, calcular_total, guardar_historial

carrito = []
productos = obtener_productos()

def actualizar_total():
    total = calcular_total(carrito)
    total_label.config(text=f"Total: ${total}")

def agregar():
    producto_nombre = combo_producto.get()
    cantidad = entry_cantidad.get()

    if not producto_nombre or not cantidad:
        messagebox.showerror("Error", "Selecciona un producto y una cantidad válida.")
        return

    try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError

        agregar_al_carrito(carrito, producto_nombre, cantidad)
        messagebox.showinfo("Agregado", f"{producto_nombre} x{cantidad} añadido al carrito.")
        actualizar_total()
        entry_cantidad.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Cantidad inválida o mayor al stock disponible.")

def finalizar():
    if not carrito:
        messagebox.showwarning("Vacío", "El carrito está vacío.")
        return

    resumen = "\n".join(f"{p['nombre']} x{p['cantidad']} = ${p['precio']*p['cantidad']}" for p in carrito)
    total = calcular_total(carrito)
    messagebox.showinfo("Compra finalizada", f"{resumen}\n\nTotal: ${total}")

    guardar_historial(carrito)
    carrito.clear()
    actualizar_total()

def ver_historial():
    try:
        with open("historial.txt", "r") as f:
            ventas = f.readlines()
    except FileNotFoundError:
        ventas = []

    historial_ventana = tk.Toplevel(root)
    historial_ventana.title("Historial de Ventas")

    tree = ttk.Treeview(historial_ventana, columns=("Producto", "Cantidad", "Total"), show="headings")
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Total", text="Total")
    tree.pack(fill=tk.BOTH, expand=True)

    total_ganancia = 0
    for venta in ventas:
        nombre, cantidad, total = venta.strip().split(", ")
        total_ganancia += int(total)
        tree.insert("", tk.END, values=(nombre, cantidad, f"${total}"))

    tk.Label(historial_ventana, text=f"Ganancia total: ${total_ganancia}", font=("Arial", 12, "bold")).pack(pady=5)

# ---- INTERFAZ ----
root = tk.Tk()
root.title("Caja Registradora Fruber")

tk.Label(root, text="Producto:").grid(row=0, column=0, padx=5, pady=5)
combo_producto = ttk.Combobox(root, values=[p["nombre"] for p in productos])
combo_producto.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

btn_agregar = tk.Button(root, text="Agregar al carrito", command=agregar)
btn_agregar.grid(row=2, column=0, columnspan=2, pady=10)

total_label = tk.Label(root, text="Total: $0", font=("Arial", 12))
total_label.grid(row=3, column=0, columnspan=2)

btn_finalizar = tk.Button(root, text="Finalizar compra", command=finalizar)
btn_finalizar.grid(row=4, column=0, padx=5, pady=10)

btn_historial = tk.Button(root, text="Ver historial de ventas", command=ver_historial)
btn_historial.grid(row=4, column=1, padx=5, pady=10)

root.mainloop()

