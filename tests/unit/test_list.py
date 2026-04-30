import pytest
from src.objects.list import DoublyLinkedList, OUT_OF_BOUNDS


class TestDoublyLinkedList:
    def setup_method(self):
        self.dll = DoublyLinkedList()

    # --- TESTS PARA append(value) ---
    def test_cp_lista_01_insertar_valor_valido(self):
        """RF05: Insertar cadena de texto válida al final de lista vacía."""
        self.dll.append("Data1")
        assert self.dll.get_size() == 1
        assert self.dll.get(0) == "Data1"

    def test_cp_lista_02_insertar_multiples_valores(self):
        """RF05: Insertar cadena de texto válida en lista con elementos previos."""
        self.dll.append("Data1")
        self.dll.append("Data2")
        assert self.dll.get_size() == 2
        assert self.dll.get(1) == "Data2"

    def test_cp_lista_03_insertar_cadena_vacia(self):
        """RF05: Insertar cadena de texto vacía."""
        self.dll.append("")
        assert self.dll.get_size() == 1
        assert self.dll.get(0) == ""

    def test_cp_lista_04_insertar_cadena_larga(self):
        """RF05: Insertar cadena de texto extremadamente larga (Límite MAX simulado)."""
        cadena_larga = "A" * 10000
        self.dll.append(cadena_larga)
        assert self.dll.get_size() == 1
        assert self.dll.get(0) == cadena_larga

    def test_cp_lista_05_insertar_valor_nulo_invalido(self):
        """RF05: Insertar valor None (puntero nulo), debe lanzar excepción o ser rechazado."""
        with pytest.raises(ValueError, match="El valor no puede ser None"):
            self.dll.append(None)
        assert self.dll.get_size() == 0

    # --- TESTS PARA get(position) ---
    def test_cp_lista_06_obtener_posicion_cero_limite(self):
        """RF06: Obtener valor en índice 0 (límite inferior válido)."""
        self.dll.append("A")
        assert self.dll.get(0) == "A"

    def test_cp_lista_07_obtener_posicion_intermedia_valida(self):
        """RF06: Obtener valor en posición intermedia."""
        self.dll.append("A")
        self.dll.append("B")
        self.dll.append("C")
        assert self.dll.get(1) == "B"

    def test_cp_lista_08_obtener_posicion_superior_limite(self):
        """RF06: Obtener valor en el último índice (límite superior válido size-1)."""
        self.dll.append("A")
        self.dll.append("B")
        assert self.dll.get(self.dll.get_size() - 1) == "B"

    def test_cp_lista_09_obtener_fuera_rango_inferior_limite(self):
        """RF06: Obtener índice -1 (fuera de límite inferior)."""
        self.dll.append("A")
        assert self.dll.get(-1) == OUT_OF_BOUNDS

    def test_cp_lista_10_obtener_fuera_rango_superior_limite(self):
        """RF06: Obtener índice igual al tamaño (fuera de límite superior)."""
        self.dll.append("A")
        assert self.dll.get(1) == OUT_OF_BOUNDS
        assert self.dll.get(2) == OUT_OF_BOUNDS

    # --- TESTS PARA remove(position) ---
    def test_cp_lista_11_remover_cabeza_limite(self):
        """RF07: Remover elemento en posición 0."""
        self.dll.append("A")
        self.dll.append("B")
        removido = self.dll.remove(0)
        assert removido == "A"
        assert self.dll.get_size() == 1
        assert self.dll.get(0) == "B"

    def test_cp_lista_12_remover_cola_limite(self):
        """RF07: Remover elemento en el último índice (size-1)."""
        self.dll.append("A")
        self.dll.append("B")
        removido = self.dll.remove(1)
        assert removido == "B"
        assert self.dll.get_size() == 1
        assert self.dll.get(0) == "A"

    def test_cp_lista_13_remover_medio(self):
        """RF07: Remover elemento en posición intermedia."""
        self.dll.append("A")
        self.dll.append("B")
        self.dll.append("C")
        removido = self.dll.remove(1)
        assert removido == "B"
        assert self.dll.get_size() == 2
        assert self.dll.get(0) == "A"
        assert self.dll.get(1) == "C"

    def test_cp_lista_14_remover_fuera_rango_inferior(self):
        """RF07: Remover elemento en índice -1."""
        self.dll.append("A")
        assert self.dll.remove(-1) == OUT_OF_BOUNDS
        assert self.dll.get_size() == 1

    def test_cp_lista_15_remover_fuera_rango_superior(self):
        """RF07: Remover elemento en índice size."""
        self.dll.append("A")
        assert self.dll.remove(1) == OUT_OF_BOUNDS
        assert self.dll.get_size() == 1

    # --- TESTS PARA get_size() ---
    def test_cp_lista_16_tamano_vacia(self):
        """RF08: Obtener tamaño de lista vacía."""
        assert self.dll.get_size() == 0

    def test_cp_lista_17_tamano_un_elemento(self):
        """RF08: Obtener tamaño tras una inserción."""
        self.dll.append("A")
        assert self.dll.get_size() == 1

    def test_cp_lista_18_tamano_multiples_elementos(self):
        """RF08: Obtener tamaño tras múltiples inserciones."""
        for i in range(5):
            self.dll.append(str(i))
        assert self.dll.get_size() == 5

    def test_cp_lista_19_tamano_tras_remover(self):
        """RF08: Obtener tamaño tras inserciones y remociones."""
        self.dll.append("A")
        self.dll.append("B")
        self.dll.remove(0)
        assert self.dll.get_size() == 1

    def test_cp_lista_20_tamano_remover_invalido(self):
        """RF08: El tamaño no debe cambiar tras intento de remoción fallido."""
        self.dll.append("A")
        self.dll.remove(10)
        assert self.dll.get_size() == 1

    # --- TESTS PARA contains(value) ---
    def test_cp_lista_21_contiene_existente_cabeza(self):
        """RF09: Buscar valor existente ubicado al principio."""
        self.dll.append("A")
        self.dll.append("B")
        assert self.dll.contains("A") is True

    def test_cp_lista_22_contiene_existente_cola(self):
        """RF09: Buscar valor existente ubicado al final."""
        self.dll.append("A")
        self.dll.append("B")
        assert self.dll.contains("B") is True

    def test_cp_lista_23_contiene_inexistente(self):
        """RF09: Buscar valor que no está en la lista."""
        self.dll.append("A")
        assert self.dll.contains("C") is False

    def test_cp_lista_24_contiene_en_lista_vacia(self):
        """RF09: Buscar valor en lista vacía."""
        assert self.dll.contains("A") is False

    def test_cp_lista_25_contiene_valor_nulo_invalido(self):
        """RF09: Buscar valor nulo (None)."""
        self.dll.append("A")
        assert self.dll.contains(None) is False
