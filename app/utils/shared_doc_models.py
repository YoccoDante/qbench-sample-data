from flask_restx import fields


def create_doc_models(api):
    # Request body model
    get_sample_data_body_model = api.model('GetSampleDataRequest', {
        'sample_id': fields.Integer(required=True, description='ID of the sample data to fetch')
    })

    # Response model
    get_sample_data_response_model = api.model('GetSampleDataResponse', {
        'id': fields.Integer(description='The unique identifier of the data'),
        'content': fields.String(description='The content of the data'),
        'created_at': fields.DateTime(description='Timestamp when the data was created'),
        'updated_at': fields.DateTime(description='Timestamp when the data was last updated')
    })

    error_response_model = api.model(
        "ErrorResponse",
        {
            "data": fields.Raw(default=None, description="The payload of the error response (null for errors)."),
            "message": fields.String(description="Descriptive message about the error."),
            "status": fields.String(description="Status of the response, e.g., 'error'."),
        },
    )

    return {
        "get_sample_data_body_model": get_sample_data_body_model,
        "get_sample_data_response_model": get_sample_data_response_model,
        "error_response_model": error_response_model
    }