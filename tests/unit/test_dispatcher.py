import pytest
from unittest.mock import MagicMock
from src.server.object_server import ServidorObjetos
from src.server.dispatcher import Despachador
from src.objects.tree import ExcepcionValorDuplicado


class TestDespachador:
    def setup_method(self):
        self.servidor = ServidorObjetos()
        self.despachador = Despachador(self.servidor)

    # --- GRUPO 1: Operaciones Globales del Servidor (create / destroy) ---
    def test_cp_despachador_01_create_ok(self):
        """Comando create exitoso para un nuevo objeto."""
        comando = {"object": "list", "operation": "create", "id": "obj1", "data": ""}
        resp = self.despachador.procesar_comando(comando)
        assert resp == {"object": "list", "operation": "create", "id": "obj1", "data": "OK"}

    def test_cp_despachador_02_create_ya_existe(self):
        """Comando create para un ID que ya existe retorna ERROR_YA_EXISTE."""
        self.servidor.crear_objeto("list", "obj_existente")
        comando = {"object": "stack", "operation": "create", "id": "obj_existente", "data": ""}
        resp = self.despachador.procesar_comando(comando)
        assert resp["data"] == "ERROR_YA_EXISTE"

    def test_cp_despachador_03_create_tipo_desconocido(self):
        """Comando create con un tipo de objeto no soportado retorna ERROR_TIPO_DESCONOCIDO."""
        comando = {"object": "invalido", "operation": "create", "id": "obj_err", "data": ""}
        resp = self.despachador.procesar_comando(comando)
        assert resp["data"] == "ERROR_TIPO_DESCONOCIDO"

    def test_cp_despachador_04_destroy_ok(self):
        """Comando destroy exitoso sobre un objeto existente."""
        self.servidor.crear_objeto("tree", "obj_del")
        comando = {"object": "tree", "operation": "destroy", "id": "obj_del", "data": ""}
        resp = self.despachador.procesar_comando(comando)
        assert resp["data"] == "OK"

    def test_cp_despachador_05_destroy_no_existe(self):
        """Comando destroy sobre un ID inexistente retorna ERROR_NO_EXISTE."""
        comando = {"object": "list", "operation": "destroy", "id": "fantasma", "data": ""}
        resp = self.despachador.procesar_comando(comando)
        assert resp["data"] == "ERROR_NO_EXISTE"

    # --- GRUPO 2: Enrutamiento y Validaciones Generales ---
    def test_cp_despachador_06_comando_vacio(self):
        """Procesar un comando vacío o incompleto."""
        resp = self.despachador.procesar_comando({})
        assert resp["data"] == "ERROR_NO_EXISTE"

    def test_cp_despachador_07_objeto_no_existe(self):
        """Enviar una operación de colección a un ID no registrado."""
        comando = {"object": "list", "operation": "append", "id": "no_creado", "data": "10"}
        resp = self.despachador.procesar_comando(comando)
        assert resp["data"] == "ERROR_NO_EXISTE"

    def test_cp_despachador_08_tipo_incoherente_al_despachar(self):
        """El objeto existe pero el tipo en el comando es desconocido para las ramas internas."""
        self.servidor.crear_objeto("list", "obj_incoherente")
        # Inyectamos un comando con object distinto para forzar la rama de ERROR_TIPO_DESCONOCIDO en sección crítica
        comando = {"object": "matriz", "operation": "append", "id": "obj_incoherente", "data": "10"}
        resp = self.despachador.procesar_comando(comando)
        assert resp["data"] == "ERROR_TIPO_DESCONOCIDO"

    def test_cp_despachador_09_operacion_desconocida(self):
        """Operación no soportada por la estructura específica."""
        self.servidor.crear_objeto("list", "obj_lista")
        comando = {"object": "list", "operation": "invertir", "id": "obj_lista", "data": ""}
        resp = self.despachador.procesar_comando(comando)
        assert resp["data"] == "ERROR_OPERACION_INVALIDA"

    def test_cp_despachador_10_captura_excepcion_generica(self):
        """Simular una falla interna no prevista para verificar el retorno de ERROR_INTERNO."""
        self.servidor.crear_objeto("list", "obj_fallo")
        instancia, lock = self.servidor.obtener_objeto("obj_fallo")
        # Sobrescribimos temporalmente el método append con un mock que lance Exception
        instancia.append = MagicMock(side_effect=Exception("Falla catastrófica simulada"))
        comando = {"object": "list", "operation": "append", "id": "obj_fallo", "data": "10"}
        resp = self.despachador.procesar_comando(comando)
        assert resp["data"] == "ERROR_INTERNO"

    # --- GRUPO 3: Despacho a Lista (list) ---
    def test_cp_despachador_11_lista_append(self):
        """Despacho correcto de la operación append en una lista."""
        self.servidor.crear_objeto("list", "l1")
        comando = {"object": "list", "operation": "append", "id": "l1", "data": "ItemA"}
        assert self.despachador.procesar_comando(comando)["data"] == "OK"

    def test_cp_despachador_12_lista_size(self):
        """Despacho correcto de la operación size en una lista."""
        self.servidor.crear_objeto("list", "l1")
        self.despachador.procesar_comando({"object": "list", "operation": "append", "id": "l1", "data": "A"})
        comando = {"object": "list", "operation": "size", "id": "l1", "data": ""}
        assert self.despachador.procesar_comando(comando)["data"] == "1"

    def test_cp_despachador_13_lista_get(self):
        """Despacho correcto de la operación get en una lista."""
        self.servidor.crear_objeto("list", "l1")
        self.despachador.procesar_comando({"object": "list", "operation": "append", "id": "l1", "data": "A"})
        assert self.despachador.procesar_comando({"object": "list", "operation": "get", "id": "l1", "data": "0"})["data"] == "A"

    def test_cp_despachador_14_lista_remove(self):
        """Despacho correcto de la operación remove en una lista."""
        self.servidor.crear_objeto("list", "l1")
        self.despachador.procesar_comando({"object": "list", "operation": "append", "id": "l1", "data": "A"})
        assert self.despachador.procesar_comando({"object": "list", "operation": "remove", "id": "l1", "data": "0"})["data"] == "A"

    def test_cp_despachador_15_lista_contains(self):
        """Despacho correcto de la operación contains en una lista."""
        self.servidor.crear_objeto("list", "l1")
        self.despachador.procesar_comando({"object": "list", "operation": "append", "id": "l1", "data": "Target"})
        assert self.despachador.procesar_comando({"object": "list", "operation": "contains", "id": "l1", "data": "Target"})["data"] == "True"

    # --- GRUPO 4: Despacho a Pila (stack) ---
    def test_cp_despachador_16_pila_push(self):
        """Despacho correcto de la operación push en una pila."""
        self.servidor.crear_objeto("stack", "p1")
        assert self.despachador.procesar_comando({"object": "stack", "operation": "push", "id": "p1", "data": "X"})["data"] == "OK"

    def test_cp_despachador_17_pila_pop(self):
        """Despacho correcto de la operación pop en una pila."""
        self.servidor.crear_objeto("stack", "p1")
        self.despachador.procesar_comando({"object": "stack", "operation": "push", "id": "p1", "data": "X"})
        assert self.despachador.procesar_comando({"object": "stack", "operation": "pop", "id": "p1", "data": ""})["data"] == "X"

    def test_cp_despachador_18_pila_peek(self):
        """Despacho correcto de la operación peek en una pila."""
        self.servidor.crear_objeto("stack", "p1")
        self.despachador.procesar_comando({"object": "stack", "operation": "push", "id": "p1", "data": "Tope"})
        assert self.despachador.procesar_comando({"object": "stack", "operation": "peek", "id": "p1", "data": ""})["data"] == "Tope"

    def test_cp_despachador_19_pila_isempty(self):
        """Despacho correcto de la operación isempty en una pila."""
        self.servidor.crear_objeto("stack", "p1")
        assert self.despachador.procesar_comando({"object": "stack", "operation": "isempty", "id": "p1", "data": ""})["data"] == "True"

    def test_cp_despachador_20_pila_vacia_pop(self):
        """Hacer pop de una pila vacía retorna la constante configurada en la pila."""
        self.servidor.crear_objeto("stack", "p1")
        assert self.despachador.procesar_comando({"object": "stack", "operation": "pop", "id": "p1", "data": ""})["data"] == "EMPTY_STRUCTURE"

    # --- GRUPO 5: Despacho a Árbol (tree) ---
    def test_cp_despachador_21_arbol_insert(self):
        """Despacho de insert en árbol con valor numérico (debe convertirse a entero)."""
        self.servidor.crear_objeto("tree", "t1")
        assert self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t1", "data": "50"})["data"] == "OK"

    def test_cp_despachador_22_arbol_search(self):
        """Despacho de search en árbol."""
        self.servidor.crear_objeto("tree", "t1")
        self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t1", "data": "50"})
        assert self.despachador.procesar_comando({"object": "tree", "operation": "search", "id": "t1", "data": "50"})["data"] == "True"

    def test_cp_despachador_23_arbol_delete(self):
        """Despacho de delete en árbol."""
        self.servidor.crear_objeto("tree", "t1")
        self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t1", "data": "50"})
        assert self.despachador.procesar_comando({"object": "tree", "operation": "delete", "id": "t1", "data": "50"})["data"] == "OK"

    def test_cp_despachador_24_arbol_inorder(self):
        """Despacho de inorder en árbol retorna cadena separada por comas."""
        self.servidor.crear_objeto("tree", "t1")
        self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t1", "data": "50"})
        self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t1", "data": "30"})
        assert self.despachador.procesar_comando({"object": "tree", "operation": "inorder", "id": "t1", "data": ""})["data"] == "30,50"

    def test_cp_despachador_25_arbol_height(self):
        """Despacho de height en árbol."""
        self.servidor.crear_objeto("tree", "t1")
        self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t1", "data": "50"})
        assert self.despachador.procesar_comando({"object": "tree", "operation": "height", "id": "t1", "data": ""})["data"] == "1"

    def test_cp_despachador_26_arbol_duplicado(self):
        """Captura de ExcepcionValorDuplicado retornando ERROR_VALOR_DUPLICADO."""
        self.servidor.crear_objeto("tree", "t1")
        self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t1", "data": "50"})
        resp = self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t1", "data": "50"})
        assert resp["data"] == "ERROR_VALOR_DUPLICADO"

    def test_cp_despachador_27_arbol_valor_invalido(self):
        """Captura de ValueError retornando ERROR_VALOR_INVALIDO."""
        self.servidor.crear_objeto("tree", "t1")
        instancia, lock = self.servidor.obtener_objeto("t1")
        # Forzamos un ValueError mockeando insertar
        instancia.insertar = MagicMock(side_effect=ValueError("Valor nulo no permitido"))
        resp = self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t1", "data": "None"})
        assert resp["data"] == "ERROR_VALOR_INVALIDO"


    def test_cp_despachador_28_arbol_eliminar_inexistente(self):
        """Intento de eliminar un valor que no existe en el árbol. Debe retornar ERROR_VALOR_NO_ENCONTRADO."""
        self.servidor.crear_objeto("tree", "t_elim")
        self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t_elim", "data": "10"})
        resp = self.despachador.procesar_comando({"object": "tree", "operation": "delete", "id": "t_elim", "data": "99"})
        assert resp["data"] == "ERROR_VALOR_NO_ENCONTRADO"

    def test_cp_despachador_29_arbol_conflicto_tipos(self):
        """Intento de mezclar tipos (letras en un árbol de números). Debe retornar ERROR_TIPO_INVALIDO."""
        self.servidor.crear_objeto("tree", "t_tipos")
        self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t_tipos", "data": "5"})
        resp = self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "t_tipos", "data": "Hola"})
        assert resp["data"] == "ERROR_TIPO_INVALIDO"

    def test_cp_despachador_30_pila_rechazar_negativos(self):
        """Intento de apilar un número negativo en la pila. Debe retornar ERROR_VALOR_NEGATIVO."""
        self.servidor.crear_objeto("stack", "p_neg")
        resp = self.despachador.procesar_comando({"object": "stack", "operation": "push", "id": "p_neg", "data": "-5"})
        assert resp["data"] == "ERROR_VALOR_NEGATIVO"
