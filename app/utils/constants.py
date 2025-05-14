from enum import Enum

class APIResponse(Enum):
    ACCESS_RESTRICTED = "Access Restricted"
    OPERATION_SUCCESS = "Operation success"
    UNEXPECTED_ERROR = "Unexpected error occurred"
    NOT_FOUND = "Entity or resource not found"
    INVALID_REQUEST = "Invalid request"

class RequestKeys(Enum):
    MESSAGE = "message"
    STATUS = "status"
    DATA = "data"
    CODE = "code"
