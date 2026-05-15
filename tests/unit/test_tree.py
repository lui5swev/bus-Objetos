import pytest
from src.objects.tree import ArbolBinarioBusqueda, ExcepcionValorDuplicado


class TestArbolBinarioBusqueda:
    def setup_method(self):
        self.arbol = ArbolBinarioBusqueda()

    # --- TESTS PARA insertar(valor) ---
    def test_cp_arbol_01_insertar_raiz(self):
        """Insertar el primer elemento en un árbol vacío (Raíz)."""
        self.arbol.insertar(10)
        assert self.arbol.raiz is not None
        assert self.arbol.raiz.valor == 10
        assert self.arbol.raiz.izquierdo is None
        assert self.arbol.raiz.derecho is None

    def test_cp_arbol_02_insertar_menor_izquierdo(self):
        """Insertar un valor menor que la raíz, debe ubicarse a la izquierda."""
        self.arbol.insertar(10)
        self.arbol.insertar(5)
        assert self.arbol.raiz.izquierdo is not None
        assert self.arbol.raiz.izquierdo.valor == 5

    def test_cp_arbol_03_insertar_mayor_derecho(self):
        """Insertar un valor mayor que la raíz, debe ubicarse a la derecha."""
        self.arbol.insertar(10)
        self.arbol.insertar(15)
        assert self.arbol.raiz.derecho is not None
        assert self.arbol.raiz.derecho.valor == 15

    def test_cp_arbol_04_insertar_duplicado_excepcion(self):
        """Insertar un valor ya existente debe lanzar ExcepcionValorDuplicado."""
        self.arbol.insertar(10)
        with pytest.raises(ExcepcionValorDuplicado, match="ya existe en el árbol"):
            self.arbol.insertar(10)

    def test_cp_arbol_05_insertar_nulo_excepcion(self):
        """Insertar un valor None debe lanzar ValueError."""
        with pytest.raises(ValueError, match="El valor no puede ser None"):
            self.arbol.insertar(None)

    def test_cp_arbol_06_insertar_multiples_niveles(self):
        """Insertar múltiples valores para formar un árbol multinivel."""
        valores = [10, 5, 15, 3, 7, 12, 18]
        for v in valores:
            self.arbol.insertar(v)
        assert self.arbol.inorden() == sorted(valores)

    # --- TESTS PARA buscar(valor) ---
    def test_cp_arbol_07_buscar_en_arbol_vacio(self):
        """Buscar un valor en un árbol completamente vacío retorna False."""
        assert self.arbol.buscar(10) is False

    def test_cp_arbol_08_buscar_raiz(self):
        """Buscar el valor ubicado en la raíz retorna True."""
        self.arbol.insertar(20)
        assert self.arbol.buscar(20) is True

    def test_cp_arbol_09_buscar_hoja(self):
        """Buscar un valor ubicado en un nodo hoja retorna True."""
        self.arbol.insertar(20)
        self.arbol.insertar(10)
        self.arbol.insertar(30)
        assert self.arbol.buscar(10) is True
        assert self.arbol.buscar(30) is True

    def test_cp_arbol_10_buscar_inexistente(self):
        """Buscar un valor que no ha sido insertado retorna False."""
        self.arbol.insertar(20)
        self.arbol.insertar(10)
        assert self.arbol.buscar(15) is False

    def test_cp_arbol_11_buscar_valores_negativos(self):
        """Buscar valores numéricos negativos y frontera."""
        self.arbol.insertar(0)
        self.arbol.insertar(-5)
        assert self.arbol.buscar(-5) is True
        assert self.arbol.buscar(0) is True

    # --- TESTS PARA eliminar(valor) ---
    def test_cp_arbol_12_eliminar_hoja(self):
        """Caso 1: Eliminar un nodo hoja (sin hijos)."""
        self.arbol.insertar(10)
        self.arbol.insertar(5)
        self.arbol.eliminar(5)
        assert self.arbol.buscar(5) is False
        assert self.arbol.raiz.izquierdo is None

    def test_cp_arbol_13_eliminar_nodo_con_un_hijo(self):
        """Caso 2: Eliminar un nodo que tiene exactamente un hijo."""
        self.arbol.insertar(10)
        self.arbol.insertar(5)
        self.arbol.insertar(3)  # Nodo 5 tiene solo hijo izquierdo (3)
        self.arbol.eliminar(5)
        assert self.arbol.buscar(5) is False
        assert self.arbol.raiz.izquierdo.valor == 3

    def test_cp_arbol_14_eliminar_nodo_con_dos_hijos(self):
        """Caso 3: Eliminar un nodo con dos hijos (reemplazo por sucesor inorden)."""
        valores = [10, 5, 15, 12, 18, 13]
        for v in valores:
            self.arbol.insertar(v)
        # Nodo 15 tiene dos hijos: izquierdo (12 con hijo 13) y derecho (18)
        # Sucesor inorden de 15 es el menor del subárbol derecho, o sea 18 (en este caso el subárbol derecho de 15 es 18)
        # Espera, veamos los hijos de 15: izq=12, der=18. El mínimo del subárbol derecho de 15 es 18.
        self.arbol.eliminar(15)
        assert self.arbol.buscar(15) is False
        assert self.arbol.inorden() == [5, 10, 12, 13, 18]

    def test_cp_arbol_15_eliminar_raiz(self):
        """Eliminar el nodo raíz del árbol."""
        self.arbol.insertar(10)
        self.arbol.insertar(5)
        self.arbol.insertar(15)
        self.arbol.eliminar(10)
        assert self.arbol.buscar(10) is False
        # La nueva raíz debe ser el sucesor inorden (15) o reestructurarse correctamente
        assert self.arbol.inorden() == [5, 15]

    def test_cp_arbol_16_eliminar_inexistente(self):
        """Eliminar un valor que no existe no altera el árbol."""
        self.arbol.insertar(10)
        self.arbol.insertar(5)
        self.arbol.eliminar(99)
        assert self.arbol.inorden() == [5, 10]

    def test_cp_arbol_17_eliminar_en_arbol_vacio(self):
        """Eliminar en un árbol vacío no arroja errores."""
        self.arbol.eliminar(10)
        assert self.arbol.raiz is None

    # --- TESTS PARA inorden() ---
    def test_cp_arbol_18_inorden_vacio(self):
        """Recorrido inorden de un árbol vacío retorna lista vacía."""
        assert self.arbol.inorden() == []

    def test_cp_arbol_19_inorden_un_elemento(self):
        """Recorrido inorden de un solo elemento."""
        self.arbol.insertar(42)
        assert self.arbol.inorden() == [42]

    def test_cp_arbol_20_inorden_ordenado(self):
        """Recorrido inorden retorna los elementos numéricos ordenados de menor a mayor."""
        valores = [50, 30, 70, 20, 40, 60, 80]
        for v in valores:
            self.arbol.insertar(v)
        assert self.arbol.inorden() == sorted(valores)

    def test_cp_arbol_21_inorden_cadenas(self):
        """Recorrido inorden con cadenas de texto (orden lexicográfico)."""
        cadenas = ["banana", "manzana", "cereza", "avellana"]
        for c in cadenas:
            self.arbol.insertar(c)
        assert self.arbol.inorden() == sorted(cadenas)

    def test_cp_arbol_22_inorden_tras_eliminar(self):
        """Recorrido inorden refleja el estado correcto tras inserciones y borrados."""
        self.arbol.insertar(10)
        self.arbol.insertar(5)
        self.arbol.insertar(15)
        self.arbol.eliminar(5)
        assert self.arbol.inorden() == [10, 15]

    # --- TESTS PARA altura() ---
    def test_cp_arbol_23_altura_vacio(self):
        """La altura de un árbol vacío es 0."""
        assert self.arbol.altura() == 0

    def test_cp_arbol_24_altura_raiz(self):
        """La altura de un árbol con solo la raíz es 1."""
        self.arbol.insertar(10)
        assert self.arbol.altura() == 1

    def test_cp_arbol_25_altura_lineal(self):
        """La altura de un árbol degenerado (tipo lista enlazada) es igual a N."""
        for i in range(5):
            self.arbol.insertar(i)
        assert self.arbol.altura() == 5

    def test_cp_arbol_26_altura_balanceado(self):
        """La altura de un árbol balanceado con 3 niveles."""
        # Nivel 1: 10
        # Nivel 2: 5, 15
        # Nivel 3: 3, 7, 12, 18
        valores = [10, 5, 15, 3, 7, 12, 18]
        for v in valores:
            self.arbol.insertar(v)
        assert self.arbol.altura() == 3

    def test_cp_arbol_27_altura_tras_eliminar(self):
        """La altura se actualiza correctamente al eliminar el nivel más profundo."""
        self.arbol.insertar(10)
        self.arbol.insertar(5)
        assert self.arbol.altura() == 2
        self.arbol.eliminar(5)
        assert self.arbol.altura() == 1

    def test_cp_arbol_28_buscar_valor_nulo_lanza_error(self):
        """Buscar un valor None en el árbol debe lanzar ValueError."""
        self.arbol.insertar(10)
        with pytest.raises(ValueError, match="El valor a buscar no puede ser None"):
            self.arbol.buscar(None)
