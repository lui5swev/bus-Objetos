import threading
import pytest
from src.server.object_server import ServidorObjetos
from src.objects.list import DoublyLinkedList
from src.objects.stack import DynamicStack
from src.objects.tree import ArbolBinarioBusqueda


class TestServidorObjetos:
    def setup_method(self):
        self.servidor = ServidorObjetos()

    # --- TESTS PARA crear_objeto(tipo_objeto, id_objeto) ---
    def test_cp_servidor_01_crear_lista(self):
        """Crear un objeto de tipo 'list' exitosamente."""
        exito = self.servidor.crear_objeto("list", "obj_lista_1")
        assert exito is True
        assert "obj_lista_1" in self.servidor.registro
        assert isinstance(self.servidor.registro["obj_lista_1"]["instancia"], DoublyLinkedList)

    def test_cp_servidor_02_crear_pila(self):
        """Crear un objeto de tipo 'stack' exitosamente."""
        exito = self.servidor.crear_objeto("stack", "obj_pila_1")
        assert exito is True
        assert isinstance(self.servidor.registro["obj_pila_1"]["instancia"], DynamicStack)

    def test_cp_servidor_03_crear_arbol(self):
        """Crear un objeto de tipo 'tree' exitosamente."""
        exito = self.servidor.crear_objeto("tree", "obj_arbol_1")
        assert exito is True
        assert isinstance(self.servidor.registro["obj_arbol_1"]["instancia"], ArbolBinarioBusqueda)

    def test_cp_servidor_04_crear_duplicado(self):
        """Intentar crear un objeto con un ID ya existente debe retornar False."""
        self.servidor.crear_objeto("list", "obj_dup")
        exito = self.servidor.crear_objeto("stack", "obj_dup")
        assert exito is False
        # Debe mantenerse la instancia original (list)
        assert isinstance(self.servidor.registro["obj_dup"]["instancia"], DoublyLinkedList)

    def test_cp_servidor_05_crear_tipo_desconocido(self):
        """Intentar crear un objeto de un tipo no soportado lanza ValueError."""
        with pytest.raises(ValueError, match="Tipo de objeto desconocido"):
            self.servidor.crear_objeto("grafo", "obj_invalido")
        assert "obj_invalido" not in self.servidor.registro

    def test_cp_servidor_06_crear_case_insensitive(self):
        """La creación debe ser insensible a mayúsculas/minúsculas en el tipo."""
        exito1 = self.servidor.crear_objeto("LIST", "id1")
        exito2 = self.servidor.crear_objeto("Stack", "id2")
        assert exito1 is True
        assert exito2 is True
        assert isinstance(self.servidor.registro["id1"]["instancia"], DoublyLinkedList)
        assert isinstance(self.servidor.registro["id2"]["instancia"], DynamicStack)

    # --- TESTS PARA obtener_objeto(id_objeto) ---
    def test_cp_servidor_07_obtener_existente(self):
        """Obtener correctamente la instancia y su cerrojo (Lock) asociado."""
        self.servidor.crear_objeto("list", "id_get")
        resultado = self.servidor.obtener_objeto("id_get")
        assert resultado is not None
        instancia, lock = resultado
        assert isinstance(instancia, DoublyLinkedList)
        assert isinstance(lock, type(threading.Lock()))

    def test_cp_servidor_08_obtener_inexistente(self):
        """Consultar un ID que no existe en el registro retorna None."""
        assert self.servidor.obtener_objeto("id_fantasma") is None

    def test_cp_servidor_09_obtener_independencia_locks(self):
        """Verificar que dos objetos distintos posean cerrojos totalmente independientes."""
        self.servidor.crear_objeto("list", "id_A")
        self.servidor.crear_objeto("list", "id_B")
        _, lock_A = self.servidor.obtener_objeto("id_A")
        _, lock_B = self.servidor.obtener_objeto("id_B")
        assert lock_A is not lock_B

    def test_cp_servidor_10_obtener_consistencia_instancia(self):
        """Múltiples llamadas a obtener_objeto devuelven exactamente la misma referencia."""
        self.servidor.crear_objeto("stack", "id_consistente")
        inst1, lock1 = self.servidor.obtener_objeto("id_consistente")
        inst2, lock2 = self.servidor.obtener_objeto("id_consistente")
        assert inst1 is inst2
        assert lock1 is lock2

    def test_cp_servidor_11_obtener_tras_creacion_masiva(self):
        """Obtener objetos correctamente en un registro con múltiples elementos."""
        for i in range(10):
            self.servidor.crear_objeto("tree", f"tree_{i}")
        inst, _ = self.servidor.obtener_objeto("tree_5")
        assert isinstance(inst, ArbolBinarioBusqueda)

    # --- TESTS PARA eliminar_objeto(id_objeto) ---
    def test_cp_servidor_12_eliminar_existente(self):
        """Eliminar un objeto existente del registro exitosamente."""
        self.servidor.crear_objeto("list", "id_del")
        assert self.servidor.eliminar_objeto("id_del") is True
        assert self.servidor.obtener_objeto("id_del") is None

    def test_cp_servidor_13_eliminar_inexistente(self):
        """Intentar eliminar un ID que no existe retorna False."""
        assert self.servidor.eliminar_objeto("id_inexistente") is False

    def test_cp_servidor_14_eliminar_recrear(self):
        """Eliminar un objeto y luego recrear uno nuevo usando el mismo ID."""
        self.servidor.crear_objeto("list", "id_reuso")
        self.servidor.eliminar_objeto("id_reuso")
        exito = self.servidor.crear_objeto("stack", "id_reuso")
        assert exito is True
        inst, _ = self.servidor.obtener_objeto("id_reuso")
        assert isinstance(inst, DynamicStack)

    def test_cp_servidor_15_eliminar_vacio(self):
        """Llamar a eliminar_objeto cuando el servidor está completamente vacío."""
        assert self.servidor.eliminar_objeto("cualquier_id") is False

    def test_cp_servidor_16_eliminar_aislamiento(self):
        """Eliminar un objeto no afecta la disponibilidad del resto en el registro."""
        self.servidor.crear_objeto("list", "id_1")
        self.servidor.crear_objeto("stack", "id_2")
        self.servidor.eliminar_objeto("id_1")
        assert self.servidor.obtener_objeto("id_2") is not None

    def test_cp_servidor_17_crear_objeto_id_vacio_lanza_error(self):
        """Intentar crear un objeto con ID vacío debe lanzar ValueError."""
        with pytest.raises(ValueError, match="El ID no puede estar vacío"):
            self.servidor.crear_objeto("list", "")

    def test_cp_servidor_18_crear_objeto_limite_capacidad(self):
        """El servidor no debe permitir crear más de 100 objetos para proteger la memoria."""
        for i in range(100):
            self.servidor.crear_objeto("list", f"obj_{i}")
        exito = self.servidor.crear_objeto("list", "obj_extra")
        assert exito is False, "El servidor permitió exceder la capacidad máxima"
