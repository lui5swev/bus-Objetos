# Plan de Ejecución: Integración, Concurrencia y Pruebas (Etapa 2)

Este documento establece la hoja de ruta paso a paso para cumplir exitosamente con todos los criterios de evaluación de la **Etapa 2**, garantizando la máxima calidad de software, cumplimiento estricto de concurrencia (*thread-safety*) y una trazabilidad completa de las pruebas unitarias y de integración.

---

## Fase 1: Completar Cobertura Unitaria Estricta (Unit Testing)
Aseguraremos que todos los módulos base (incluyendo el servidor y el despachador) tengan un 100% de cobertura unitaria aislada, aplicando rigurosamente **Particiones de Equivalencia** y **Análisis de Valores Límite** con un estándar mínimo de **$\ge 5$ pruebas por función**.

* **Hito 1.1:** Creación de `tests/unit/test_tree.py`.
  * Pruebas para `insertar` ($\ge 5$ casos: árbol vacío, menor, mayor, colisión/duplicado con excepción, múltiples niveles).
  * Pruebas para `buscar` ($\ge 5$ casos: raíz, hoja, intermedio, inexistente, árbol vacío).
  * Pruebas para `eliminar` ($\ge 5$ casos: nodo sin hijos, con hijo izquierdo, con hijo derecho, con dos hijos usando sucesor inorden, inexistente).
  * Pruebas para `inorden` y `altura` ($\ge 5$ casos combinados en distintas topologías).
* **Hito 1.2:** Creación de `tests/unit/test_object_server.py`.
  * Pruebas para `crear_objeto` ($\ge 5$ casos: tipos válidos `list`/`stack`/`tree`, ID duplicado rechazado, tipo inválido lanza `ValueError`).
  * Pruebas para `obtener_objeto` ($\ge 5$ casos: consulta exitosa retorna tupla `(instancia, lock)`, consulta de ID inexistente retorna `None`, múltiples accesos).
  * Pruebas para `eliminar_objeto` ($\ge 5$ casos: borrado exitoso, borrado de ID inexistente, verificación de liberación del registro).
* **Hito 1.3:** Creación de `tests/unit/test_dispatcher.py` (usando stubs/mocks unitarios para aislarlo de la red y del servidor real si corresponde, o probando la lógica pura de despacho).
  * Pruebas de enrutamiento y comandos globales (`create`, `destroy`) con propagación de respuestas estandarizadas ($\ge 5$ casos).
  * Pruebas de despacho hacia operaciones de Lista, Pila y Árbol verificando manejo de excepciones de negocio ($\ge 5$ casos por tipo de objeto despachado).

---

## Fase 2: Sistema Unificado de Registro de Pruebas (Logging)
* **Actualización de `tests/conftest.py`:** Reforzaremos el archivo de configuración global de `pytest` para asegurar que **todas** las pruebas (unitarias, de integración y de sistema/concurrencia) queden fielmente registradas en un archivo centralizado (`tests/logs/test_runs.log`).
* El formato del log incluirá el identificador completo del nodo de prueba (`nodeid`), diferenciando claramente si pertenece a la suite `unit/`, `integration/` o `system/`, el resultado exacto (`PASSED`, `FAILED`, `ERROR`) y marcas de tiempo por sesión.

---

## Fase 3: Documentación Formal del Plan de Integración
Redacción del documento técnico exigido por la rúbrica (`plan_de_integracion.md` en la raíz del proyecto).
* **Estrategia de Integración:** Justificación técnica de la estrategia elegida (ej. **Bottom-Up** validando primero Servidor y Estructuras con Drivers antes de acoplar el Dispatcher y Serializer, o combinada con **Top-Down** mediante Stubs de red).
* **Diagrama de Dependencias:** Representación gráfica del orden de acoplamiento usando sintaxis Mermaid.
* **Análisis Comparativo:** Evaluación comparativa de las estrategias *Top-Down*, *Bottom-Up* y *Big Bang* aplicadas al contexto de un bus de objetos.
* **Gestión de Defectos:** Formato y registro de todos los defectos detectados durante la integración simulando la estructura de **GitHub Issues** (Severidad, Pasos para reproducir, Estado actual).

---

## Fase 4: Desarrollo de Stubs y Drivers para Integración
Creación de arneses de prueba determinísticos y documentados bajo `tests/integration/`.
* **Stub de Red (`StubSocket`):** Simulará la capa de transporte inyectando tramas de texto predefinidas para evaluar la interoperabilidad del `Dispatcher` y el `Serializer` sin requerir puertos abiertos.
* **Driver de Servidor (`DriverObjectServer`):** Módulo controlador que instanciará e invocará directamente al `ServidorObjetos` de forma programática para someter a carga y verificar la capa de almacenamiento eludiendo el Dispatcher.

---

## Fase 5: Casos de Prueba de Integración por Interfaz ($\ge 3$ por interfaz)
Implementación de la suite de integración en `tests/integration/test_interfaces.py` verificando los contratos entre subsistemas:
1. **Interfaz Serializer ↔ Dispatcher:** Tramas de texto convertidas a comandos y devueltas como tramas de respuesta.
2. **Interfaz Dispatcher ↔ ObjectServer:** Creación/destrucción exitosa y fallida por colisiones o inexistencia de IDs.
3. **Interfaz Dispatcher ↔ Estructuras (List / Stack / Tree):** Mutación de estado de las colecciones y propagación correcta de códigos de error hacia el despachador.

---

## Fase 6: Certificación Thread-Safe y Pruebas Multi-hilo masivas
Asegurar que el servidor y el acceso a los objetos sean completamente seguros en entornos concurrentes.
* **Auditoría de Mutexes:** Confirmar que el cerrojo global del registro (`lock_registro`) y los cerrojos individuales por objeto (`lock`) protejan todas las secciones críticas de manera robusta.
* **Prueba de Esfuerzo Concurrente (`tests/system/test_concurrency.py`):**
   * Lanzar $\ge 10$ hilos simultáneos realizando operaciones de escritura/lectura altamente competitivas sobre las mismas estructuras y sobre estructuras independientes.
   * Aserciones determinísticas: Verificar unicidad de identificadores, consistencia exacta del estado y ausencia de corrupción o interbloqueos.
