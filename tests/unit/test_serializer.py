import pytest
from src.protocol.serializer import Serializer, INVALID_MESSAGE


class TestSerializer:
    # --- TESTS PARA deserialize(message) ---
    def test_cp_serializador_01_deserializar_valido(self):
        """RF20: Deserializar un mensaje correcto y completo."""
        message = "List|Append|Req123|HelloWorld\n"
        result = Serializer.deserialize(message)
        assert result != INVALID_MESSAGE
        assert result["object"] == "List"
        assert result["operation"] == "Append"
        assert result["id"] == "Req123"
        assert result["data"] == "HelloWorld"

    def test_cp_serializador_02_deserializar_sin_salto_linea(self):
        """RF21: Mensaje malformado sin el carácter de fin de línea (límite)."""
        message = "List|Append|Req123|HelloWorld"
        result = Serializer.deserialize(message)
        assert result == INVALID_MESSAGE

    def test_cp_serializador_03_deserializar_faltan_campos(self):
        """RF21: Mensaje malformado con cantidad incorrecta de separadores."""
        message = "List|Append|Req123\n"
        result = Serializer.deserialize(message)
        assert result == INVALID_MESSAGE

    def test_cp_serializador_04_deserializar_campos_vacios(self):
        """RF21: Mensaje malformado con campos obligatorios vacíos."""
        message = "|Append|Req123|Data\n"
        result = Serializer.deserialize(message)
        assert result == INVALID_MESSAGE

    def test_cp_serializador_05_deserializar_nulo(self):
        """RF21: Mensaje nulo (None) o tipo incorrecto."""
        with pytest.raises(TypeError):
            Serializer.deserialize(None)

    def test_cp_serializador_06_deserializar_datos_vacios_valido(self):
        """RF21: Mensaje válido donde el campo de datos está vacío (ej. Pop)."""
        message = "Stack|Pop|Req1|\n"
        result = Serializer.deserialize(message)
        assert result != INVALID_MESSAGE
        assert result["data"] == ""

    # --- TESTS PARA serialize(response_dict) ---
    def test_cp_serializador_07_serializar_exito_completo(self):
        """RF22: Formatear respuesta exitosa completa."""
        response_dict = {
            "object": "List",
            "operation": "Append",
            "id": "Req123",
            "data": "Success"
        }
        result = Serializer.serialize(response_dict)
        assert result == "List|Append|Req123|Success\n"

    def test_cp_serializador_08_serializar_error(self):
        """RF23: Formatear respuesta de error."""
        response_dict = {
            "object": "Stack",
            "operation": "Pop",
            "id": "Req999",
            "data": "EMPTY_STRUCTURE"
        }
        result = Serializer.serialize(response_dict)
        assert result == "Stack|Pop|Req999|EMPTY_STRUCTURE\n"

    def test_cp_serializador_09_serializar_diccionario_incompleto(self):
        """RF22: Formatear cuando el diccionario le faltan llaves (manejo de defaults)."""
        response_dict = {
            "id": "Req1"
        }
        result = Serializer.serialize(response_dict)
        assert result == "||Req1|\n"

    def test_cp_serializador_10_serializar_diccionario_vacio(self):
        """RF22: Formatear diccionario completamente vacío (límite inferior)."""
        response_dict = {}
        result = Serializer.serialize(response_dict)
        assert result == "|||\n"

    def test_cp_serializador_11_serializar_diccionario_nulo(self):
        """RF22: Intentar serializar un diccionario nulo (None)."""
        with pytest.raises(AttributeError):
            Serializer.serialize(None)
