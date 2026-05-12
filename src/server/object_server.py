import threading
from typing import Dict, Any, Tuple, Optional

from src.objects.list import DoublyLinkedList
from src.objects.stack import DynamicStack
from src.objects.tree import ArbolBinarioBusqueda

class ServidorObjetos:
    """
    Gestiona el registro global de instancias de objetos (Listas, Pilas, Árboles).
    Utiliza un threading.Lock global para proteger el registro y asegura
    que cada objeto tenga su propio mutex individual para evitar condiciones de carrera.
    """
    def __init__(self) -> None:
        self.registro: Dict[str, Dict[str, Any]] = {}
        self.lock_registro = threading.Lock()

    def crear_objeto(self, tipo_objeto: str, id_objeto: str) -> bool:
        """
        Crea un nuevo objeto del tipo especificado y lo guarda en el registro.
        Retorna True si fue creado con éxito, False si ya existía un objeto con ese ID.
        """
        with self.lock_registro:
            if id_objeto in self.registro:
                return False
                
            instancia = None
            tipo = tipo_objeto.lower()
            if tipo == "list":
                instancia = DoublyLinkedList()
            elif tipo == "stack":
                instancia = DynamicStack()
            elif tipo == "tree":
                instancia = ArbolBinarioBusqueda()
            else:
                raise ValueError(f"Tipo de objeto desconocido: {tipo_objeto}")
                
            self.registro[id_objeto] = {
                "instancia": instancia,
                "lock": threading.Lock()  # Mutex individual para este objeto
            }
            return True

    def obtener_objeto(self, id_objeto: str) -> Optional[Tuple[Any, threading.Lock]]:
        """
        Obtiene la instancia del objeto y su mutex individual a partir del ID.
        Retorna una tupla (instancia, lock) o None si no existe.
        """
        with self.lock_registro:
            if id_objeto in self.registro:
                entrada = self.registro[id_objeto]
                return entrada["instancia"], entrada["lock"]
            return None

    def eliminar_objeto(self, id_objeto: str) -> bool:
        """
        Elimina un objeto del registro utilizando su ID.
        Retorna True si fue eliminado, False si no existía.
        """
        with self.lock_registro:
            if id_objeto in self.registro:
                del self.registro[id_objeto]
                return True
            return False
