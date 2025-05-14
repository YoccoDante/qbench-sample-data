import logging

from flask import request
from flask_restx import Namespace, Resource

from app.controllers.data import get_sample_data_by_id
from app.utils.constants import APIResponse
from app.utils.http_status_codes import HttpStatusCode
from app.utils.response_builder import ResponseBuilder
from app.utils.shared_doc_models import create_doc_models

logger = logging.getLogger(__name__)

data_ns = Namespace("data", description="Data operations")

shared_response_models = create_doc_models(data_ns)
error_response_model = shared_response_models["error_response_model"]


@data_ns.route("/sample")
class SampleDataResource(Resource):
    @data_ns.doc(
        summary="Get Sample data by id",
        description="This endpoint receives a sample_id and fetches its data from the database.",
    )
    @data_ns.expect(shared_response_models["get_sample_data_body_model"])
    @data_ns.response(
        HttpStatusCode.SUCCESS.value,
        APIResponse.OPERATION_SUCCESS.value,
        model=shared_response_models["get_sample_data_response_model"]
    )
    @data_ns.response(HttpStatusCode.BAD_REQUEST.value, APIResponse.INVALID_REQUEST.value, model=error_response_model)
    @data_ns.response(HttpStatusCode.NOT_FOUND.value, APIResponse.NOT_FOUND.value, model=error_response_model)
    @data_ns.response(HttpStatusCode.INTERNAL_SERVER_ERROR.value, APIResponse.UNEXPECTED_ERROR.value, model=error_response_model)
    def post(self):
        data = request.get_json()
        if not data or "sample_id" not in data:
            return ResponseBuilder.fail(message="No body or not sample_id in the request", status_code=HttpStatusCode.BAD_REQUEST.value)

        sample_id = data["sample_id"]
        logger.debug(f"Sample data adquisition request received, sample_id: {sample_id}")
        response = get_sample_data_by_id(sample_id)

        return response
