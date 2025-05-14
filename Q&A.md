# QBench Take-Home Answers

## 1. Jinja Template Fix and Explanation

### Original Code:

```jinja2
<section class="sample_attachments">
  {% for sample in order.samples %}
    {% set index_counter.c = index_counter.c + loop.index0 %}
    {% for attachment in sample.get_attachments() %}
      {% set index_counter.c = index_counter.c + loop.index0 %}
      {{attachment.asset.name}}-attachment
    {% endfor %}
  {% endfor %}
  {% set index_counter = namespacers(my_cool_counter===1|int|string) %}
</section>
```

### Issues and Fix:

* `index_counter` is used before it is defined. In Jinja2, you must define the `namespace` first.
* `namespacers` is not valid. The correct syntax is `namespace()`.
* The expression `my_cool_counter===1|int|string` is syntactically invalid.

### Corrected Version:

```jinja2
{% set index_counter = namespace(c=0) %}
<section class="sample_attachments">
  {% for sample in order.samples %}
    {% set index_counter.c = index_counter.c + loop.index0 %}
    {% for attachment in sample.get_attachments() %}
      {% set index_counter.c = index_counter.c + loop.index0 %}
      {{ attachment.asset.name }}-attachment<br>
    {% endfor %}
  {% endfor %}
</section>
```

## 2. Python Function Explanation

```python
import boto3
from .logger import LOG
ssm = boto3.client('ssm')

def get_param(name, WithDecryption=True):
    value = None
    try:
        value = ssm.get_parameter(
            Name=name,
            WithDecryption=WithDecryption
        )['Parameter']['Value']
    except Exception:
        LOG.warning(f"Could not fetch parameter: {name}")
    return value
```

### Description:

This helper function retrieves a parameter from AWS Systems Manager Parameter Store. It uses the `boto3` SSM client to fetch the value by `name`, with optional decryption. If an error occurs, it logs a warning and returns `None`.

### Contextual Use:

This function is likely part of a larger config service like `MySSMService`, e.g., `MySSMService.get_sqlalchemy_uri()`.

This approach is clear and functional. Could be slightly improved by handling specific exceptions.

## 3. AWS Lambda YAML Template Review

### Provided YAML:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  This is my lambda function
Globals:
  Function:
    Timeout: 60

Resources:
  MainFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: handler
      Handler: app.app.lambda_handler
      Runtime: python3.9
      Architectures:
        - x86_64
      Role: arn:aws:iam::XXXXXXXXXXXX:role/LambdaRoleHelloWorld
      Events:
        SNSEvent:
          Type: SNS
          Properties:
            Topic:  # MISSING VALUE
      Environment:
        Variables:
          IS_LOCAL: false
          QBENCH_API_CLIENT_ID: ""
          QBENCH_API_CLIENT_SECRET: ""

Outputs:
  MainFunction:
    Description: "Send results to HelloWorld"
    Value: !GetAtt MainFunction.Arn
```

### Issues Identified:

1. The `Topic` value under `SNSEvent` is missing. It needs a valid SNS Topic ARN or logical reference.
2. Role ARN has placeholder `XXXXXXXXXXXX` — this needs to be replaced or dynamically injected using `!ImportValue` or environment-specific values.
3. `QBENCH_API_CLIENT_ID` and `QBENCH_API_CLIENT_SECRET` are empty — these should be either injected from AWS SSM or provided via CI/CD.

### Valid Trigger:

* The Lambda is triggered by **Amazon SNS**, which allows invoking the function when a message is published to a topic.

### Enhancements:

* Use environment variables from SSM via code at runtime:

```python
import os
from my_module.ssm import get_param
CLIENT_ID = get_param(os.environ['QBENCH_API_CLIENT_ID'])
```

* Alternatively, use `!ImportValue` or `!Ref` in CloudFormation for shared values.

## 4. Endpoint for sample data retrieval by sample_id

> **REPOSITORY NOTE**  
> The complete implementation of this endpoint and all associated components can be found in the GitHub repository:  
> https://github.com/YoccoDante/qbench-sample-data.git

### Implementation Overview

The solution consists of several layers following clean architecture principles:

1. **API Layer** (`app/api/data.py`):
```python
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
```

2. **Controller Layer** (`app/controllers/data.py`):
```python
def get_sample_data_by_id(sample_id: int):
    try:
        logger.info(f"Getting data from sample_id: {sample_id}")
        sample_data = DataRepository.get_sample_data_by_id(sample_id)
        
        if not sample_data:
            logger.warning(f"No sample data for id: {sample_id}")
            return ResponseBuilder.fail(message=f"No sample data for id: {sample_id}")
        
        logger.info(f"Data obtained successfully for sample_id: {sample_id}")
        return ResponseBuilder.success(data=sample_data)
    except Exception:
        logger.error(f"Something went wrong while fetching data for sample_id: {sample_id}")
        return ResponseBuilder.error(
            message=f"Something went wrong while fetching data for sample_id: {sample_id}"
        )
```

3. **Repository Layer** (`app/repositories/data_repository.py`):
```python
class DataRepository:
    @staticmethod
    def get_sample_data_by_id(sample_id):
        """        
        :param sample_id: Integer representing the data to be fetched.
        :return: the sample data.
        """
        query = Data.query
        return query.filter(Data.id == sample_id).first()
```

### Features:
- Clean architecture with separation of concerns
- Comprehensive error handling
- Swagger documentation
- Input validation
- Proper logging at each layer
- Type hints for better code clarity
- Standardized response format using ResponseBuilder

## 5. Jinja2 template display for tests using filters

> **REPOSITORY NOTE**  
> The complete implementation of this template and all associated components can be found in the GitHub repository:  
> https://github.com/YoccoDante/qbench-sample-data.git

### Implementation

The solution uses Jinja2's sorting filters to display test data sorted by sample ID and assay ID:

```jinja2
{# Define the test data #}
{% set my_tests = [
    {
        "id": 10,
        "assay": {
            "id": 3,
            "title": "Assay #3",
            "description": "This assay is used for frontend testing"
        },
        "sample": {
            "id": 3,
            "sample_name": "Tigger"
        }
    },
    ...
] %}

{# Display sorted test data #}
{% for test in my_tests|sort(attribute='sample.id')|sort(attribute='assay.id') %}
    {{ test.id }} - {{ test.assay.title }} - {{ test.sample.id }}
{% endfor %}
```

### Key Features:
- Uses Jinja2's `sort` filter with `attribute` parameter
- Chained sorting (first by sample.id, then by assay.id)
- Clean output format with "-" separator
- Simple line break separation as requested
- Maintains data structure while sorting

### Output Format:
```
test_id - assay_title - sample_id
```

The template produces sorted output where:
1. Primary sort is by sample ID
2. Secondary sort is by assay ID within each sample ID group
3. Each line displays the test ID, assay title, and sample ID separated by dashes