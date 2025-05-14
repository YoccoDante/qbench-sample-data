from typing import Any, Optional

from flask import jsonify, make_response

from app.utils.constants import RequestKeys
from app.utils.http_status_codes import HttpStatusCode


class ResponseBuilder:
    @staticmethod
    def success(message: str = "Operation successful", data: Any = None, status_code: int = HttpStatusCode.SUCCESS.value):
        response_data = {
            RequestKeys.STATUS.value: "success",
            RequestKeys.MESSAGE.value: message,
            RequestKeys.DATA.value: data
        }

        return make_response(jsonify(response_data), status_code)

    @staticmethod
    def fail(message: str = "Operation failed", data: Optional[Any] = None, status_code: int = HttpStatusCode.BAD_REQUEST.value):
        response_data = {
            RequestKeys.STATUS.value: "fail",
            RequestKeys.MESSAGE.value: message,
            RequestKeys.DATA.value: data
        }
        
        return make_response(jsonify(response_data), status_code)

    @staticmethod
    def error(
        message: str = "Internal server error",
        code: Optional[str] = None,
        data: Optional[Any] = None,
        status_code: int = HttpStatusCode.INTERNAL_SERVER_ERROR.value,
    ):
        response_data = {
            RequestKeys.STATUS.value: "error",
            RequestKeys.MESSAGE.value: message,
            RequestKeys.DATA.value: data
        }

        if code:
            response_data[RequestKeys.CODE.value] = code

        return make_response(jsonify(response_data), status_code)
