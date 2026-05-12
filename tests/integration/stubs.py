from typing import List


class StubSocket:
    """
    Stub determinístico que simula un socket de red o flujo de entrada/salida.
    Permite inyectar tramas predefinidas para desacoplar las pruebas de integración
    del Dispatcher y Serializer de la capa de transporte física.
    """
    def __init__(self, tramas_entrada: List[str] = None) -> None:
        self.tramas_entrada = tramas_entrada if tramas_entrada is not None else []
        self.tramas_salida: List[str] = []
        self.indice_actual = 0

    def recibir_trama(self) -> str:
        """
        Simula la recepción de una trama desde la red.
        Retorna la siguiente cadena en la lista predefinida o una cadena vacía si no hay más.
        """
        if self.indice_actual < len(self.tramas_entrada):
            trama = self.tramas_entrada[self.indice_actual]
            self.indice_actual += 1
            return trama
        return ""

    def enviar_trama(self, trama: str) -> None:
        """
        Simula el envío de una respuesta a través de la red, almacenándola
        en un buffer interno para su posterior aserción determinística.
        """
        self.tramas_salida.append(trama)

    def reiniciar(self) -> None:
        """Reinicia el estado del stub para reutilización en múltiples pruebas."""
        self.indice_actual = 0
        self.tramas_salida.clear()
