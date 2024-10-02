import unittest
from gestor_gastos import GestorGastos

class TestGestorGastos(unittest.TestCase):

    def setUp(self):
        self.gestor = GestorGastos()
        print("\nIniciando nuevo test...")

    def test_agregar_transaccion_ingreso(self):
        print("Test: Agregar transacción de ingreso")
        self.gestor.agregar_transaccion("ingreso", "salario", 1000)
        self.assertEqual(len(self.gestor.transacciones), 1, "Debe haber exactamente una transacción.")
        self.assertEqual(self.gestor.transacciones[0]['tipo'], 'ingreso', "El tipo de la transacción debe ser 'ingreso'.")
        self.assertEqual(self.gestor.transacciones[0]['categoria'], 'salario', "La categoría debe ser 'salario'.")
        self.assertEqual(self.gestor.transacciones[0]['monto'], 1000, "El monto debe ser 1000.")
        print("Transacción de ingreso agregada correctamente.")

    def test_agregar_transaccion_gasto(self):
        print("Test: Agregar transacción de gasto")
        self.gestor.agregar_transaccion("gasto", "comida", 200)
        self.assertEqual(len(self.gestor.transacciones), 1, "Debe haber exactamente una transacción.")
        self.assertEqual(self.gestor.transacciones[0]['tipo'], 'gasto', "El tipo de la transacción debe ser 'gasto'.")
        self.assertEqual(self.gestor.transacciones[0]['categoria'], 'comida', "La categoría debe ser 'comida'.")
        self.assertEqual(self.gestor.transacciones[0]['monto'], 200, "El monto debe ser 200.")
        print("Transacción de gasto agregada correctamente.")

    def test_obtener_balance(self):
        print("Test: Verificar balance")
        self.gestor.agregar_transaccion("ingreso", "salario", 1000)
        self.gestor.agregar_transaccion("gasto", "comida", 200)
        balance = self.gestor.obtener_balance()
        self.assertEqual(balance, 800, "El balance debe ser 800.")
        print(f"Balance verificado correctamente: {balance}.")

    def test_generar_informe(self):
        print("Test: Generar informe completo")
        self.gestor.agregar_transaccion("ingreso", "salario", 1000)
        self.gestor.agregar_transaccion("gasto", "comida", 200)
        informe = self.gestor.generar_informe()
        self.assertIn("Informe de Gastos", informe, "El informe debe contener el título 'Informe de Gastos'.")
        self.assertIn("salario", informe, "El informe debe contener la categoría 'salario'.")
        self.assertIn("comida", informe, "El informe debe contener la categoría 'comida'.")
        self.assertIn("Balance actual: 800", informe, "El balance en el informe debe ser 800.")
        print("Informe generado correctamente:\n", informe)

    def test_generar_informe_por_categoria(self):
        print("Test: Generar informe por categoría")
        self.gestor.agregar_transaccion("ingreso", "salario", 1000)
        self.gestor.agregar_transaccion("gasto", "comida", 200)
        informe_categoria = self.gestor.generar_informe_por_categoria("comida")
        self.assertIn("Categoría: comida", informe_categoria, "El informe debe contener la categoría 'comida'.")
        self.assertIn("Gastos: 200", informe_categoria, "El informe debe mostrar los gastos en 'comida'.")
        self.assertIn("Balance total: -200", informe_categoria, "El balance para 'comida' debe ser -200.")
        print("Informe por categoría generado correctamente:\n", informe_categoria)

    def test_informe_todas_categorias(self):
        print("Test: Generar informe para todas las categorías")
        self.gestor.agregar_transaccion("ingreso", "salario", 1000)
        self.gestor.agregar_transaccion("gasto", "comida", 200)
        informe_categoria = self.gestor.generar_informe_por_categoria()
        self.assertIn("Categoría: salario", informe_categoria, "El informe debe contener la categoría 'salario'.")
        self.assertIn("Categoría: comida", informe_categoria, "El informe debe contener la categoría 'comida'.")
        self.assertIn("Balance total: 800", informe_categoria, "El balance total debe ser 800.")
        print("Informe para todas las categorías generado correctamente:\n", informe_categoria)

if __name__ == '__main__':
    unittest.main()
