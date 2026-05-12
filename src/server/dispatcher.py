from typing import Dict, Any
from src.server.object_server import ServidorObjetos
from src.objects.tree import ExcepcionValorDuplicado

class Despachador:
    """
    Controlador desacoplado que procesa los comandos parseados del protocolo
    y se comunica con el ServidorObjetos para ejecutar las acciones.
    Agnóstico de la red, diseñado para facilitar las pruebas con stubs.
    """
    def __init__(self, servidor: ServidorObjetos) -> None:
        self.servidor = servidor

    def procesar_comando(self, comando: Dict[str, str]) -> Dict[str, str]:
        """
        Recibe un diccionario con el comando parseado y ejecuta la operación solicitada.
        Retorna un diccionario de respuesta.
        """
        obj_tipo = comando.get("object", "").lower()
        operacion = comando.get("operation", "").lower()
        req_id = comando.get("id", "")
        data = comando.get("data", "")
        
        # Formato de respuesta por defecto
        respuesta = {
            "object": obj_tipo,
            "operation": operacion,
            "id": req_id,
            "data": "ERROR_DESCONOCIDO"
        }
        
        # Operaciones de nivel de servidor (crear/eliminar)
        if operacion == "create":
            try:
                exito = self.servidor.crear_objeto(obj_tipo, req_id)
                respuesta["data"] = "OK" if exito else "ERROR_YA_EXISTE"
            except ValueError:
                respuesta["data"] = "ERROR_TIPO_DESCONOCIDO"
            return respuesta
            
        if operacion == "destroy":
            exito = self.servidor.eliminar_objeto(req_id)
            respuesta["data"] = "OK" if exito else "ERROR_NO_EXISTE"
            return respuesta

        # Para las demás operaciones, necesitamos obtener el objeto y su mutex
        resultado = self.servidor.obtener_objeto(req_id)
        if not resultado:
            respuesta["data"] = "ERROR_NO_EXISTE"
            return respuesta
            
        instancia, lock = resultado
        
        # Sección crítica: Adquirimos el mutex individual del objeto
        with lock:
            try:
                if obj_tipo == "list":
                    respuesta["data"] = self._procesar_lista(instancia, operacion, data)
                elif obj_tipo == "stack":
                    respuesta["data"] = self._procesar_pila(instancia, operacion, data)
                elif obj_tipo == "tree":
                    respuesta["data"] = self._procesar_arbol(instancia, operacion, data)
                else:
                    respuesta["data"] = "ERROR_TIPO_DESCONOCIDO"
                    
            except ExcepcionValorDuplicado:
                respuesta["data"] = "ERROR_VALOR_DUPLICADO"
            except ValueError:
                respuesta["data"] = "ERROR_VALOR_INVALIDO"
            except Exception as e:
                respuesta["data"] = "ERROR_INTERNO"
                
        return respuesta

    def _procesar_lista(self, instancia: Any, operacion: str, data: str) -> str:
        if operacion == "append":
            instancia.append(data)
            return "OK"
        elif operacion == "get":
            val = instancia.get(int(data))
            return str(val)
        elif operacion == "remove":
            val = instancia.remove(int(data))
            return str(val)
        elif operacion == "size":
            return str(instancia.get_size())
        elif operacion == "contains":
            return str(instancia.contains(data))
        else:
            return "ERROR_OPERACION_INVALIDA"

    def _procesar_pila(self, instancia: Any, operacion: str, data: str) -> str:
        if operacion == "push":
            instancia.push(data)
            return "OK"
        elif operacion == "pop":
            val = instancia.pop()
            return str(val)
        elif operacion == "peek":
            val = instancia.peek()
            return str(val)
        elif operacion == "isempty":
            return str(instancia.is_empty())
        else:
            return "ERROR_OPERACION_INVALIDA"

    def _procesar_arbol(self, instancia: Any, operacion: str, data: str) -> str:
        # Convertir a entero si es numérico para permitir un ordenamiento correcto en el BST
        valor = int(data) if (data.lstrip('-').isdigit() and data != "") else data

        if operacion == "insert":
            instancia.insertar(valor)
            return "OK"
        elif operacion == "search":
            return str(instancia.buscar(valor))
        elif operacion == "delete":
            instancia.eliminar(valor)
            return "OK"
        elif operacion == "inorder":
            return ",".join(map(str, instancia.inorden()))
        elif operacion == "height":
            return str(instancia.altura())
        else:
            return "ERROR_OPERACION_INVALIDA"
