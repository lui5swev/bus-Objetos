from typing import Any, Optional, Tuple
import threading
from src.server.object_server import ServidorObjetos


class DriverObjectServer:
    """
    Driver determinístico que actúa como cliente programático directo del ServidorObjetos.
    Permite invocar de forma secuencial o concurrente las colecciones registradas
    eludiendo completamente la capa del Dispatcher, validando el almacenamiento y thread-safety.
    """
    def __init__(self, servidor: ServidorObjetos) -> None:
        self.servidor = servidor

    def inicializar_entorno(self, configuraciones: list) -> bool:
        """
        Crea masivamente objetos a partir de una lista de tuplas (tipo, id).
        Retorna True si todos fueron creados con éxito.
        """
        exito_total = True
        for tipo, id_obj in configuraciones:
            if not self.servidor.crear_objeto(tipo, id_obj):
                exito_total = False
        return exito_total

    def ejecutar_operacion_segura(self, id_obj: str, metodo: str, *args: Any) -> Tuple[bool, Optional[Any]]:
        """
        Obtiene el objeto y su mutex exclusivo desde el servidor, adquiere el cerrojo
        y ejecuta el método solicitado de forma totalmente thread-safe.
        Retorna (exito, resultado).
        """
        resultado_server = self.servidor.obtener_objeto(id_obj)
        if not resultado_server:
            return False, None

        instancia, lock = resultado_server
        with lock:
            try:
                func = getattr(instancia, metodo)
                res = func(*args)
                return True, res
            except Exception as e:
                return False, str(e)

    def destruir_entorno(self, ids: list) -> bool:
        """
        Elimina masivamente una lista de IDs del servidor.
        """
        exito = True
        for id_obj in ids:
            if not self.servidor.eliminar_objeto(id_obj):
                exito = False
        return exito
