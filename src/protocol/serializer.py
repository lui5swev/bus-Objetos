from typing import Dict, Union, Any

INVALID_MESSAGE = -1

class Serializer:
    @staticmethod
    def deserialize(message: str) -> Union[Dict[str, str], int]:
        """RF20/RF21: Parse valid requests, return error constants for malformed ones.
        Expected Format: Object|Operation|ID|Data\n
        
        NOTE: This method uses Python's str.split(), which is immutable and inherently 
        thread-safe (stateless), fulfilling the concurrency safety requirement of strtok_r.
        """
        if not isinstance(message, str):
            raise TypeError("El mensaje debe ser una cadena de texto")
        
        if not message.endswith("\n"):
            return INVALID_MESSAGE
            
        # Remove trailing newline for parsing
        content = message[:-1]
        parts = content.split("|")
        
        # We expect exactly 4 parts: Object, Operation, ID, Data
        if len(parts) != 4:
            return INVALID_MESSAGE
            
        obj, op, req_id, data = parts
        
        # Basic validation (could be expanded based on specific RF constraints)
        if not obj or not op or not req_id:
             return INVALID_MESSAGE
             
        return {
            "object": obj,
            "operation": op,
            "id": req_id,
            "data": data
        }

    @staticmethod
    def serialize(response_dict: Dict[str, str]) -> str:
        """RF22/RF23: Format success/error responses.
        Expected Output Format: Object|Operation|ID|Data\n
        """
        obj = response_dict.get("object", "")
        op = response_dict.get("operation", "")
        req_id = response_dict.get("id", "")
        data = response_dict.get("data", "")
        
        return f"{obj}|{op}|{req_id}|{data}\n"
