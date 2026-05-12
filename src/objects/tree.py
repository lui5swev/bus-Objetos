from typing import Any, List, Optional
import threading

class ExcepcionValorDuplicado(Exception):
    """Excepción lanzada cuando se intenta insertar un valor que ya existe en el árbol."""
    pass

class NodoArbol:
    def __init__(self, valor: Any) -> None:
        self.valor = valor
        self.izquierdo: Optional['NodoArbol'] = None
        self.derecho: Optional['NodoArbol'] = None

class ArbolBinarioBusqueda:
    def __init__(self) -> None:
        self.raiz: Optional[NodoArbol] = None
        self.lock = threading.Lock()

    def insertar(self, valor: Any) -> None:
        """Inserta un valor en el árbol. Lanza ExcepcionValorDuplicado si el valor ya existe."""
        if valor is None:
            raise ValueError("El valor no puede ser None")
        
        with self.lock:
            if self.raiz is None:
                self.raiz = NodoArbol(valor)
            else:
                self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo: NodoArbol, valor: Any) -> None:
        if valor == nodo.valor:
            raise ExcepcionValorDuplicado(f"El valor {valor} ya existe en el árbol")
        elif valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor)
        else:
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo.derecho, valor)

    def buscar(self, valor: Any) -> bool:
        """Busca un valor en el árbol. Retorna True si lo encuentra, False en caso contrario."""
        with self.lock:
            return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo: Optional[NodoArbol], valor: Any) -> bool:
        if nodo is None:
            return False
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo.derecho, valor)

    def eliminar(self, valor: Any) -> None:
        """Elimina un valor del árbol."""
        with self.lock:
            self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo: Optional[NodoArbol], valor: Any) -> Optional[NodoArbol]:
        if nodo is None:
            return None
            
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)
        else:
            # Nodo encontrado
            # Caso 1 y 2: Un hijo o sin hijos
            if nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo
                
            # Caso 3: Dos hijos. Obtener el sucesor inorden (el menor del subárbol derecho)
            temp = self._minimo_valor_nodo(nodo.derecho)
            nodo.valor = temp.valor
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, temp.valor)
            
        return nodo

    def _minimo_valor_nodo(self, nodo: NodoArbol) -> NodoArbol:
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def inorden(self) -> List[Any]:
        """Realiza un recorrido inorden del árbol y retorna una lista de valores."""
        with self.lock:
            resultado = []
            self._inorden_recursivo(self.raiz, resultado)
            return resultado

    def _inorden_recursivo(self, nodo: Optional[NodoArbol], resultado: List[Any]) -> None:
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_recursivo(nodo.derecho, resultado)

    def altura(self) -> int:
        """Calcula y retorna la altura del árbol."""
        with self.lock:
            return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, nodo: Optional[NodoArbol]) -> int:
        if nodo is None:
            return 0
        altura_izq = self._altura_recursiva(nodo.izquierdo)
        altura_der = self._altura_recursiva(nodo.derecho)
        return max(altura_izq, altura_der) + 1
