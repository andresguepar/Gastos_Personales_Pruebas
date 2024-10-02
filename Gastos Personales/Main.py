from collections import defaultdict
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog

# Clase que maneja la lógica de gestión de gastos
class GestorGastos:
    def __init__(self):
        # Inicializa la lista de transacciones
        self.transacciones = []

    # Método para agregar una transacción a la lista
    def agregar_transaccion(self, tipo, categoria, monto):
        # Captura la fecha actual
        fecha = datetime.date.today()
        # Agrega un diccionario con la información de la transacción
        self.transacciones.append({
            "fecha": fecha,
            "tipo": tipo,
            "categoria": categoria,
            "monto": monto
        })

    # Método que calcula el balance actual (ingresos - gastos)
    def obtener_balance(self):
        # Suma todos los ingresos
        ingresos = sum(t["monto"] for t in self.transacciones if t["tipo"] == "ingreso")
        # Suma todos los gastos
        gastos = sum(t["monto"] for t in self.transacciones if t["tipo"] == "gasto")
        # Retorna el balance (ingresos - gastos)
        return ingresos - gastos

    # Método para generar un informe detallado de todas las transacciones
    def generar_informe(self):
        informe = "--- Informe de Gastos ---\n"
        # Recorre cada transacción y la agrega al informe
        for t in self.transacciones:
            informe += f"{t['fecha']} - {t['tipo'].capitalize()}: {t['monto']} ({t['categoria']})\n"
        # Añade el balance actual al final del informe
        informe += f"\nBalance actual: {self.obtener_balance()}"
        return informe

    # Método para generar un informe filtrado por categoría
    def generar_informe_por_categoria(self, categoria=None):
        # Filtra transacciones por categoría, si se proporciona una
        if categoria:
            transacciones_filtradas = [t for t in self.transacciones if t['categoria'].lower() == categoria.lower()]
        else:
            transacciones_filtradas = self.transacciones

        # Diccionario que almacena ingresos y gastos por categoría
        categorias = defaultdict(lambda: {'ingresos': 0, 'gastos': 0})
        for t in transacciones_filtradas:
            # Si es ingreso, suma el monto a ingresos de la categoría
            if t['tipo'] == 'ingreso':
                categorias[t['categoria']]['ingresos'] += t['monto']
            # Si es gasto, suma el monto a gastos de la categoría
            else:
                categorias[t['categoria']]['gastos'] += t['monto']

        # Genera el informe por categoría
        informe = f"--- Informe {'de ' + categoria.capitalize() if categoria else 'por Categorías'} ---\n\n"
        for cat, valores in categorias.items():
            informe += f"Categoría: {cat}\n"
            informe += f"  Ingresos: {valores['ingresos']}\n"
            informe += f"  Gastos: {valores['gastos']}\n"
            informe += f"  Balance: {valores['ingresos'] - valores['gastos']}\n\n"

        # Añade el balance total al final del informe
        informe += f"Balance total: {sum(v['ingresos'] for v in categorias.values()) - sum(v['gastos'] for v in categorias.values())}"
        return informe

# Clase que maneja la interfaz gráfica de usuario (GUI)
class AplicacionGUI:
    def __init__(self, master):
        # Inicializa la ventana principal y el gestor de gastos
        self.master = master
        self.gestor = GestorGastos()

        # Configuración básica de la ventana principal
        master.title("Gestor de Gastos Personales")
        master.geometry("500x400")
        master.configure(bg="#f0f0f0")

        # Estilos personalizados para widgets de la interfaz
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.map("TButton",
            foreground=[('pressed', 'white'), ('active', 'black')],
            background=[('pressed', '!disabled', '#3c8dbc'), ('active', '#5bc0de')]
        )

        # Frame principal donde se colocarán los widgets
        self.frame = ttk.Frame(master, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Título de la aplicación
        ttk.Label(self.frame, text="Gestor de Gastos Personales", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Frame para agregar transacción
        self.trans_frame = ttk.Frame(self.frame, padding="10")
        self.trans_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.trans_frame.columnconfigure(1, weight=1)

        # Campo para seleccionar el tipo de transacción (ingreso o gasto)
        ttk.Label(self.trans_frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.tipo_var = tk.StringVar()
        self.tipo_combo = ttk.Combobox(self.trans_frame, textvariable=self.tipo_var, values=["ingreso", "gasto"])
        self.tipo_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        self.tipo_combo.set("ingreso")  # Valor por defecto

        # Campo para ingresar la categoría de la transacción
        ttk.Label(self.trans_frame, text="Categoría:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.categoria_var = tk.StringVar()
        ttk.Entry(self.trans_frame, textvariable=self.categoria_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Campo para ingresar el monto de la transacción
        ttk.Label(self.trans_frame, text="Monto:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.monto_var = tk.StringVar()
        ttk.Entry(self.trans_frame, textvariable=self.monto_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # Botón para agregar una transacción
        ttk.Button(self.trans_frame, text="Agregar Transacción", command=self.agregar_transaccion).grid(row=3, column=0, columnspan=2, pady=10)

        # Frame para los botones de acciones adicionales
        self.action_frame = ttk.Frame(self.frame, padding="10")
        self.action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Botones para ver balance, generar informe y generar informe por categoría
        ttk.Button(self.action_frame, text="Ver Balance", command=self.ver_balance).grid(row=0, column=0, padx=5)
        ttk.Button(self.action_frame, text="Generar Informe", command=self.generar_informe).grid(row=0, column=1, padx=5)
        ttk.Button(self.action_frame, text="Informe por Categoría", command=self.generar_informe_por_categoria).grid(row=0, column=2, padx=5)

    # Método que maneja el evento de agregar transacción
    def agregar_transaccion(self):
        # Obtiene los valores ingresados por el usuario
        tipo = self.tipo_var.get()
        categoria = self.categoria_var.get()
        try:
            # Intenta convertir el monto a número
            monto = float(self.monto_var.get())
        except ValueError:
            # Muestra un mensaje de error si el monto no es un número
            messagebox.showerror("Error", "El monto debe ser un número.")
            return

        # Agrega la transacción al gestor
        self.gestor.agregar_transaccion(tipo, categoria, monto)
        messagebox.showinfo("Éxito", f"Transacción agregada: {tipo} de {monto} en {categoria}")

        # Limpia los campos después de agregar la transacción
        self.tipo_var.set("ingreso")
        self.categoria_var.set("")
        self.monto_var.set("")

    # Muestra el balance actual
    def ver_balance(self):
        balance = self.gestor.obtener_balance()
        messagebox.showinfo("Balance", f"Balance actual: {balance:.2f}")

    # Genera y muestra un informe completo de todas las transacciones
    def generar_informe(self):
        informe = self.gestor.generar_informe()
        self.mostrar_informe("Informe de Gastos", informe)

    # Genera y muestra un informe filtrado por categoría
    def generar_informe_por_categoria(self):
        categoria = simpledialog.askstring("Informe por Categoría", "Ingrese la categoría (deje en blanco para todas):")
        informe = self.gestor.generar_informe_por_categoria(categoria)
        self.mostrar_informe("Informe por Categoría", informe)

    # Método auxiliar para mostrar informes en una nueva ventana
    def mostrar_informe(self, titulo, informe):
        # Crear una nueva ventana para mostrar el informe
        ventana_informe = tk.Toplevel(self.master)
        ventana_informe.title(titulo)
        ventana_informe.geometry("400x300")
        ventana_informe.configure(bg="#f0f0f0")

        # Frame para contener el texto del informe
        frame = ttk.Frame(ventana_informe, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        ventana_informe.grid_columnconfigure(0, weight=1)
        ventana_informe.grid_rowconfigure(0, weight=1)

        # Widget de texto para mostrar el informe
        texto_informe = tk.Text(frame, wrap=tk.WORD, font=("Arial", 10))
        texto_informe.insert(tk.END, informe)
        texto_informe.pack(expand=True, fill=tk.BOTH)

        # Barra de desplazamiento para el informe
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=texto_informe.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        texto_informe.configure(yscrollcommand=scrollbar.set)

# Función principal para iniciar la aplicación
def main():
    root = tk.Tk()  # Crea la ventana principal
    app = AplicacionGUI(root)  # Inicializa la aplicación con la ventana principal
    root.mainloop()  # Ejecuta el bucle principal de la interfaz

# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()
