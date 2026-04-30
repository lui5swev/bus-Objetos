import pytest
from src.objects.stack import DynamicStack, EMPTY_STRUCTURE

class TestDynamicStack:
    def setup_method(self):
        self.stack = DynamicStack()

    # --- TESTS PARA push(value) ---
    def test_cp_pila_01_apilar_valor_valido_vacia(self):
        """RF10: Apilar cadena válida en pila vacía."""
        self.stack.push("A")
        assert self.stack.peek() == "A"
        assert self.stack.is_empty() is False

    def test_cp_pila_02_apilar_multiples_valores(self):
        """RF10: Apilar cadenas en pila con elementos (límite intermedio)."""
        self.stack.push("A")
        self.stack.push("B")
        assert self.stack.peek() == "B"

    def test_cp_pila_03_apilar_cadena_vacia(self):
        """RF10: Apilar una cadena de texto vacía."""
        self.stack.push("")
        assert self.stack.peek() == ""

    def test_cp_pila_04_apilar_cadena_larga(self):
        """RF10: Apilar cadena de texto extremadamente larga (límite MAX)."""
        cadena_larga = "Z" * 10000
        self.stack.push(cadena_larga)
        assert self.stack.peek() == cadena_larga

    def test_cp_pila_05_apilar_valor_nulo_invalido(self):
        """RF10: Apilar valor nulo (None) debe lanzar excepción o ser rechazado."""
        with pytest.raises(ValueError, match="El valor no puede ser None"):
            self.stack.push(None)
        assert self.stack.is_empty() is True

    # --- TESTS PARA pop() ---
    def test_cp_pila_06_desapilar_elemento_unico_limite(self):
        """RF11: Desapilar el único elemento de la pila."""
        self.stack.push("A")
        assert self.stack.pop() == "A"
        assert self.stack.is_empty() is True

    def test_cp_pila_07_desapilar_elementos_LIFO(self):
        """RF11: Desapilar múltiples elementos en orden LIFO."""
        self.stack.push("A")
        self.stack.push("B")
        self.stack.push("C")
        assert self.stack.pop() == "C"
        assert self.stack.pop() == "B"
        assert self.stack.pop() == "A"

    def test_cp_pila_08_desapilar_pila_vacia_limite(self):
        """RF11: Intentar desapilar cuando la pila está vacía (límite inferior)."""
        assert self.stack.pop() == EMPTY_STRUCTURE

    def test_cp_pila_09_desapilar_tras_vaciar(self):
        """RF11: Desapilar luego de vaciar completamente la pila."""
        self.stack.push("A")
        self.stack.pop()
        assert self.stack.pop() == EMPTY_STRUCTURE

    def test_cp_pila_10_desapilar_intercalado_push(self):
        """RF11: Secuencia intercalada de apilar y desapilar."""
        self.stack.push("A")
        assert self.stack.pop() == "A"
        self.stack.push("B")
        assert self.stack.pop() == "B"
        assert self.stack.pop() == EMPTY_STRUCTURE

    # --- TESTS PARA peek() ---
    def test_cp_pila_11_observar_elemento_unico(self):
        """RF12: Observar el tope con un elemento."""
        self.stack.push("A")
        assert self.stack.peek() == "A"

    def test_cp_pila_12_observar_no_altera_pila(self):
        """RF12: Observar no remueve el elemento."""
        self.stack.push("A")
        self.stack.peek()
        assert self.stack.is_empty() is False
        assert self.stack.pop() == "A"

    def test_cp_pila_13_observar_pila_vacia_limite(self):
        """RF12: Intentar observar pila vacía."""
        assert self.stack.peek() == EMPTY_STRUCTURE

    def test_cp_pila_14_observar_tras_multiples_push(self):
        """RF12: Observar tope tras varios apilamientos."""
        self.stack.push("A")
        self.stack.push("B")
        assert self.stack.peek() == "B"

    def test_cp_pila_15_observar_tras_pop(self):
        """RF12: Observar tope tras un desapilado."""
        self.stack.push("A")
        self.stack.push("B")
        self.stack.pop()
        assert self.stack.peek() == "A"

    # --- TESTS PARA is_empty() ---
    def test_cp_pila_16_vacia_inicialmente(self):
        """RF13: Verificar vacía al inicializar."""
        assert self.stack.is_empty() is True

    def test_cp_pila_17_no_vacia_con_elemento(self):
        """RF13: Verificar no vacía con 1 elemento."""
        self.stack.push("A")
        assert self.stack.is_empty() is False

    def test_cp_pila_18_vacia_tras_pop(self):
        """RF13: Verificar vacía tras remover el único elemento."""
        self.stack.push("A")
        self.stack.pop()
        assert self.stack.is_empty() is True

    def test_cp_pila_19_no_vacia_multiples_elementos(self):
        """RF13: Verificar no vacía con múltiples elementos."""
        self.stack.push("A")
        self.stack.push("B")
        assert self.stack.is_empty() is False

    def test_cp_pila_20_estado_consistente_tras_error(self):
        """RF13: Verificar que peek a pila vacía no altera su estado."""
        self.stack.peek()
        assert self.stack.is_empty() is True
