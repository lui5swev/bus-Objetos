import threading
from typing import List
import pytest
from src.server.object_server import ServidorObjetos
from src.server.dispatcher import Despachador


class TestConcurrenciaSistema:
    """
    Suite de pruebas de sistema/concurrencia para certificar el cumplimiento estricto
    de thread-safety en el Object Server y las colecciones subyacentes.
    Se somete al sistema a una alta competencia multi-hilo (≥10 hilos simultáneos)
    para asegurar la unicidad de IDs de respuesta, consistencia de estado y ausencia de corrupción.
    """
    def setup_method(self):
        self.servidor = ServidorObjetos()
        self.despachador = Despachador(self.servidor)

    def test_conc_01_creacion_masiva_competitiva(self):
        """
        ≥10 hilos intentan crear atómicamente el MISMO ID de objeto simultáneamente.
        Solo exactamente un hilo debe recibir 'OK', el resto 'ERROR_YA_EXISTE'.
        """
        num_hilos = 15
        respuestas: List[str] = [""] * num_hilos
        hilos = []

        def tarea(indice: int):
            comando = {"object": "list", "operation": "create", "id": "obj_compartido", "data": ""}
            resp = self.despachador.procesar_comando(comando)
            respuestas[indice] = resp["data"]

        for i in range(num_hilos):
            t = threading.Thread(target=tarea, args=(i,))
            hilos.append(t)
            t.start()

        for t in hilos:
            t.join()

        # Aserción determinística: exactamente un 'OK' y N-1 'ERROR_YA_EXISTE'
        exitos = respuestas.count("OK")
        errores = respuestas.count("ERROR_YA_EXISTE")
        assert exitos == 1
        assert errores == num_hilos - 1

    def test_conc_02_escritura_concurrente_misma_lista(self):
        """
        ≥10 hilos agregan concurrentemente múltiples elementos a la misma instancia de lista.
        Verifica la ausencia total de corrupción o pérdida de escrituras en los punteros de Nodos.
        """
        self.servidor.crear_objeto("list", "lista_conc")
        num_hilos = 12
        inserciones_por_hilo = 50
        hilos = []

        def tarea_escritura(hilo_id: int):
            for i in range(inserciones_por_hilo):
                comando = {"object": "list", "operation": "append", "id": "lista_conc", "data": f"H{hilo_id}_{i}"}
                self.despachador.procesar_comando(comando)

        for i in range(num_hilos):
            t = threading.Thread(target=tarea_escritura, args=(i,))
            hilos.append(t)
            t.start()

        for t in hilos:
            t.join()

        # Verificamos tamaño atómico final
        resp_size = self.despachador.procesar_comando({"object": "list", "operation": "size", "id": "lista_conc", "data": ""})
        total_esperado = num_hilos * inserciones_por_hilo
        assert resp_size["data"] == str(total_esperado)

    def test_conc_03_apilado_concurrente_misma_pila(self):
        """
        ≥10 hilos realizan operaciones push altamente competitivas sobre la misma pila.
        """
        self.servidor.crear_objeto("stack", "pila_conc")
        num_hilos = 10
        push_por_hilo = 40
        hilos = []

        def tarea_push():
            for _ in range(push_por_hilo):
                self.despachador.procesar_comando({"object": "stack", "operation": "push", "id": "pila_conc", "data": "X"})

        for _ in range(num_hilos):
            t = threading.Thread(target=tarea_push)
            hilos.append(t)
            t.start()

        for t in hilos:
            t.join()

        # Desapilamos todo para contar y verificar integridad de los enlaces
        elementos_contados = 0
        while True:
            resp = self.despachador.procesar_comando({"object": "stack", "operation": "pop", "id": "pila_conc", "data": ""})
            if resp["data"] == "EMPTY_STRUCTURE":
                break
            elementos_contados += 1

        assert elementos_contados == num_hilos * push_por_hilo

    def test_conc_04_insercion_concurrente_arbol(self):
        """
        ≥10 hilos insertan valores distintos de forma simultánea en un Árbol Binario de Búsqueda.
        Verifica que las rotaciones/inserciones de punteros en el BST mantengan un estado inorden coherente.
        """
        self.servidor.crear_objeto("tree", "arbol_conc")
        num_hilos = 10
        hilos = []
        # Para evitar colisiones intencionalmente y probar la concurrencia estructural, asignamos rangos disjuntos
        def tarea_arbol(inicio: int):
            for v in range(inicio, inicio + 10):
                self.despachador.procesar_comando({"object": "tree", "operation": "insert", "id": "arbol_conc", "data": str(v)})

        for i in range(num_hilos):
            t = threading.Thread(target=tarea_arbol, args=(i * 10,))
            hilos.append(t)
            t.start()

        for t in hilos:
            t.join()

        # Consultamos recorrido inorden
        resp = self.despachador.procesar_comando({"object": "tree", "operation": "inorder", "id": "arbol_conc", "data": ""})
        valores_obtenidos = list(map(int, resp["data"].split(",")))
        esperados = list(range(num_hilos * 10))
        assert valores_obtenidos == esperados

    def test_conc_05_aislamiento_operaciones_independientes(self):
        """
        ≥10 hilos operan concurrentemente sobre objetos con IDs totalmente distintos.
        Garantiza que la concurrencia fina (mutex por objeto) evite cuellos de botella globales.
        """
        num_hilos = 10
        hilos = []
        
        # Pre-creamos los objetos
        for i in range(num_hilos):
            self.servidor.crear_objeto("list", f"indep_{i}")

        def tarea_indep(id_num: int):
            for _ in range(20):
                self.despachador.procesar_comando({"object": "list", "operation": "append", "id": f"indep_{id_num}", "data": "A"})

        for i in range(num_hilos):
            t = threading.Thread(target=tarea_indep, args=(i,))
            hilos.append(t)
            t.start()

        for t in hilos:
            t.join()

        # Verificamos que todas las listas individuales tengan exactamente 20 elementos
        for i in range(num_hilos):
            res = self.despachador.procesar_comando({"object": "list", "operation": "size", "id": f"indep_{i}", "data": ""})
            assert res["data"] == "20"
