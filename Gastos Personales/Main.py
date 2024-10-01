from collections import defaultdict
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog

class GestorGastos:
    def __init__(self):
        self.transacciones = []

    def agregar_transaccion(self, tipo, categoria, monto):
        fecha = datetime.date.today()
        self.transacciones.append({
            "fecha": fecha,
            "tipo": tipo,
            "categoria": categoria,
            "monto": monto
        })

    def obtener_balance(self):
        ingresos = sum(t["monto"] for t in self.transacciones if t["tipo"] == "ingreso")
        gastos = sum(t["monto"] for t in self.transacciones if t["tipo"] == "gasto")
        return ingresos - gastos

    def generar_informe(self):
        informe = "--- Informe de Gastos ---\n"
        for t in self.transacciones:
            informe += f"{t['fecha']} - {t['tipo'].capitalize()}: {t['monto']} ({t['categoria']})\n"
        informe += f"\nBalance actual: {self.obtener_balance()}"
        return informe

    def generar_informe_por_categoria(self, categoria=None):
        if categoria:
            transacciones_filtradas = [t for t in self.transacciones if t['categoria'].lower() == categoria.lower()]
        else:
            transacciones_filtradas = self.transacciones

        categorias = defaultdict(lambda: {'ingresos': 0, 'gastos': 0})
        for t in transacciones_filtradas:
            if t['tipo'] == 'ingreso':
                categorias[t['categoria']]['ingresos'] += t['monto']
            else:
                categorias[t['categoria']]['gastos'] += t['monto']

        informe = f"--- Informe {'de ' + categoria.capitalize() if categoria else 'por Categorías'} ---\n\n"
        for cat, valores in categorias.items():
            informe += f"Categoría: {cat}\n"
            informe += f"  Ingresos: {valores['ingresos']}\n"
            informe += f"  Gastos: {valores['gastos']}\n"
            informe += f"  Balance: {valores['ingresos'] - valores['gastos']}\n\n"

        informe += f"Balance total: {sum(v['ingresos'] for v in categorias.values()) - sum(v['gastos'] for v in categorias.values())}"
        return informe
    
class AplicacionGUI:
    def __init__(self, master):
        self.master = master
        self.gestor = GestorGastos()
        master.title("Gestor de Gastos Personales")
        master.geometry("500x400")
        master.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.map("TButton",
            foreground=[('pressed', 'white'), ('active', 'black')],
            background=[('pressed', '!disabled', '#3c8dbc'), ('active', '#5bc0de')]
        )

        # Frame principal
        self.frame = ttk.Frame(master, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Título
        ttk.Label(self.frame, text="Gestor de Gastos Personales", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Frame para agregar transacción
        self.trans_frame = ttk.Frame(self.frame, padding="10")
        self.trans_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.trans_frame.columnconfigure(1, weight=1)

        ttk.Label(self.trans_frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.tipo_var = tk.StringVar()
        self.tipo_combo = ttk.Combobox(self.trans_frame, textvariable=self.tipo_var, values=["ingreso", "gasto"])
        self.tipo_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        self.tipo_combo.set("ingreso")

        ttk.Label(self.trans_frame, text="Categoría:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.categoria_var = tk.StringVar()
        ttk.Entry(self.trans_frame, textvariable=self.categoria_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.trans_frame, text="Monto:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.monto_var = tk.StringVar()
        ttk.Entry(self.trans_frame, textvariable=self.monto_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(self.trans_frame, text="Agregar Transacción", command=self.agregar_transaccion).grid(row=3, column=0, columnspan=2, pady=10)

        # Frame para botones de acción
        self.action_frame = ttk.Frame(self.frame, padding="10")
        self.action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(self.action_frame, text="Ver Balance", command=self.ver_balance).grid(row=0, column=0, padx=5)
        ttk.Button(self.action_frame, text="Generar Informe", command=self.generar_informe).grid(row=0, column=1, padx=5)
        ttk.Button(self.action_frame, text="Informe por Categoría", command=self.generar_informe_por_categoria).grid(row=0, column=2, padx=5)

    def agregar_transaccion(self):
        tipo = self.tipo_var.get()
        categoria = self.categoria_var.get()
        try:
            monto = float(self.monto_var.get())
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número.")
            return

        self.gestor.agregar_transaccion(tipo, categoria, monto)
        messagebox.showinfo("Éxito", f"Transacción agregada: {tipo} de {monto} en {categoria}")

        # Limpiar los campos
        self.tipo_var.set("ingreso")
        self.categoria_var.set("")
        self.monto_var.set("")

    def ver_balance(self):
        balance = self.gestor.obtener_balance()
        messagebox.showinfo("Balance", f"Balance actual: {balance:.2f}")

    def generar_informe(self):
        informe = self.gestor.generar_informe()
        self.mostrar_informe("Informe de Gastos", informe)

    def generar_informe_por_categoria(self):
        categoria = simpledialog.askstring("Informe por Categoría", "Ingrese la categoría (deje en blanco para todas):")
        informe = self.gestor.generar_informe_por_categoria(categoria)
        self.mostrar_informe("Informe por Categoría", informe)

    def mostrar_informe(self, titulo, informe):
        ventana_informe = tk.Toplevel(self.master)
        ventana_informe.title(titulo)
        ventana_informe.geometry("400x300")
        ventana_informe.configure(bg="#f0f0f0")

        frame = ttk.Frame(ventana_informe, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        ventana_informe.grid_columnconfigure(0, weight=1)
        ventana_informe.grid_rowconfigure(0, weight=1)

        texto_informe = tk.Text(frame, wrap=tk.WORD, font=("Arial", 10))
        texto_informe.insert(tk.END, informe)
        texto_informe.pack(expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=texto_informe.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        texto_informe.configure(yscrollcommand=scrollbar.set)

def main():
    root = tk.Tk()
    app = AplicacionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()