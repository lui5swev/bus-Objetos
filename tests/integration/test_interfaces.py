import pytest
from src.protocol.serializer import Serializer, INVALID_MESSAGE
from src.server.object_server import ServidorObjetos
from src.server.dispatcher import Despachador
from tests.integration.stubs import StubSocket
from tests.integration.drivers import DriverObjectServer


class TestIntegracionInterfaces:
    def setup_method(self):
        self.servidor = ServidorObjetos()
        self.despachador = Despachador(self.servidor)
        self.driver = DriverObjectServer(self.servidor)

    # --- INTERFAZ 1: Serializer ↔ Dispatcher ---
    def test_integ_ser_disp_01_flujo_normal(self):
        """Tramas crudas completan ciclo exitoso de parseo, ejecución y formateo de respuesta."""
        stub = StubSocket(["list|create|id_ser_1|\n"])
        trama_in = stub.recibir_trama()
        comando = Serializer.deserialize(trama_in)
        assert isinstance(comando, dict)
        
        respuesta_dict = self.despachador.procesar_comando(comando)
        trama_out = Serializer.serialize(respuesta_dict)
        stub.enviar_trama(trama_out)
        
        assert stub.tramas_salida[0] == "list|create|id_ser_1|OK\n"

    def test_integ_ser_disp_02_trama_malformada(self):
        """Trama sin terminador de salto de línea es interceptada por el Serializer."""
        stub = StubSocket(["list|create|id_ser_2"])  # Falta \n
        trama_in = stub.recibir_trama()
        comando = Serializer.deserialize(trama_in)
        
        assert comando == INVALID_MESSAGE
        # En el bucle principal, un INVALID_MESSAGE genera una trama de error estandarizada
        trama_out = Serializer.serialize({"object": "", "operation": "", "id": "", "data": "INVALID_MESSAGE"})
        assert trama_out == "|||INVALID_MESSAGE\n"

    def test_integ_ser_disp_03_operacion_desconocida(self):
        """Trama válida con operación desconocida propaga el error hasta la trama de salida."""
        self.servidor.crear_objeto("tree", "t_ser")
        trama_in = "tree|volar|t_ser|\n"
        comando = Serializer.deserialize(trama_in)
        respuesta = self.despachador.procesar_comando(comando)
        assert Serializer.serialize(respuesta) == "tree|volar|t_ser|ERROR_OPERACION_INVALIDA\n"

    # --- INTERFAZ 2: Dispatcher ↔ ObjectServer ---
    def test_integ_disp_server_01_creacion_destruccion(self):
        """Verificar mutación del registro en el ObjectServer mediante comandos del Dispatcher."""
        assert "obj_integ" not in self.servidor.registro
        self.despachador.procesar_comando({"object": "list", "operation": "create", "id": "obj_integ", "data": ""})
        assert "obj_integ" in self.servidor.registro
        
        self.despachador.procesar_comando({"object": "list", "operation": "destroy", "id": "obj_integ", "data": ""})
        assert "obj_integ" not in self.servidor.registro

    def test_integ_disp_server_02_id_inexistente(self):
        """Comando hacia un ID no registrado es detectado consultando al servidor."""
        respuesta = self.despachador.procesar_comando({"object": "stack", "operation": "push", "id": "no_existo", "data": "A"})
        assert respuesta["data"] == "ERROR_NO_EXISTE"

    def test_integ_disp_server_03_colision_ids(self):
        """Evitar sobrescritura en el servidor ante comandos concurrentes o repetidos de creación."""
        resp1 = self.despachador.procesar_comando({"object": "stack", "operation": "create", "id": "colision", "data": ""})
        resp2 = self.despachador.procesar_comando({"object": "tree", "operation": "create", "id": "colision", "data": ""})
        
        assert resp1["data"] == "OK"
        assert resp2["data"] == "ERROR_YA_EXISTE"
        # Certificamos con el Driver que el tipo original (stack) prevaleció
        exito, is_empty = self.driver.ejecutar_operacion_segura("colision", "is_empty")
        assert exito is True
        assert is_empty is True

    # --- INTERFAZ 3: Dispatcher ↔ Estructuras (List / Stack / Tree) ---
    def test_integ_disp_estructuras_01_pila_vacia(self):
        """Propagación de error EMPTY_STRUCTURE desde DynamicStack hacia el Dispatcher."""
        self.servidor.crear_objeto("stack", "p_integ")
        resp = self.despachador.procesar_comando({"object": "stack", "operation": "pop", "id": "p_integ", "data": ""})
        assert resp["data"] == "EMPTY_STRUCTURE"

    def test_integ_disp_estructuras_02_lista_fuera_rango(self):
        """Propagación de error OUT_OF_BOUNDS desde DoublyLinkedList hacia el Dispatcher."""
        self.servidor.crear_objeto("list", "l_integ")
        self.despachador.procesar_comando({"object": "list", "operation": "append", "id": "l_integ", "data": "A"})
        resp = self.despachador.procesar_comando({"object": "list", "operation": "get", "id": "l_integ", "data": "5"})
        assert resp["data"] == "OUT_OF_BOUNDS"

    def test_integ_disp_estructuras_03_arbol_duplicado(self):
        """Propagación de ExcepcionValorDuplicado desde ArbolBinarioBusqueda hacia el Dispatcher."""
        self.servidor.crear_objeto("tree", "t_integ")
        self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t_integ", "data": "100"})
        resp = self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t_integ", "data": "100"})
        assert resp["data"] == "ERROR_VALOR_DUPLICADO"

    def test_integ_disp_estructuras_04_flujo_completo_mutacion(self):
        """Mutación de estado verificada bidireccionalmente mediante Dispatcher y Driver."""
        self.servidor.crear_objeto("list", "l_mut")
        for i in range(3):
            self.despachador.procesar_comando({"object": "list", "operation": "append", "id": "l_mut", "data": f"val_{i}"})
            
        # Comprobamos con el Driver el tamaño final
        exito, size = self.driver.ejecutar_operacion_segura("l_mut", "get_size")
        assert exito is True
        assert size == 3
