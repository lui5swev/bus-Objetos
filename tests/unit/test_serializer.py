import pytest
from src.protocol.serializer import Serializer, INVALID_MESSAGE

class TestSerializer:
    def test_tc_serializer_01_deserialize_valid(self):
        """RF20: Parse valid request."""
        message = "List|Append|Req123|HelloWorld\n"
        result = Serializer.deserialize(message)
        assert result != INVALID_MESSAGE
        assert result["object"] == "List"
        assert result["operation"] == "Append"
        assert result["id"] == "Req123"
        assert result["data"] == "HelloWorld"

    def test_tc_serializer_02_deserialize_missing_newline(self):
        """RF21: Malformed request missing newline."""
        message = "List|Append|Req123|HelloWorld"
        result = Serializer.deserialize(message)
        assert result == INVALID_MESSAGE

    def test_tc_serializer_03_deserialize_missing_fields(self):
        """RF21: Malformed request missing fields."""
        message = "List|Append|Req123\n"
        result = Serializer.deserialize(message)
        assert result == INVALID_MESSAGE

    def test_tc_serializer_04_deserialize_empty_fields(self):
        """RF21: Malformed request empty required fields."""
        message = "|Append|Req123|Data\n"
        result = Serializer.deserialize(message)
        assert result == INVALID_MESSAGE

    def test_tc_serializer_05_serialize_success(self):
        """RF22: Format success response."""
        response_dict = {
            "object": "List",
            "operation": "Append",
            "id": "Req123",
            "data": "Success"
        }
        result = Serializer.serialize(response_dict)
        assert result == "List|Append|Req123|Success\n"

    def test_tc_serializer_06_serialize_error(self):
        """RF23: Format error response."""
        response_dict = {
            "object": "Stack",
            "operation": "Pop",
            "id": "Req999",
            "data": "EMPTY_STRUCTURE"
        }
        result = Serializer.serialize(response_dict)
        assert result == "Stack|Pop|Req999|EMPTY_STRUCTURE\n"
