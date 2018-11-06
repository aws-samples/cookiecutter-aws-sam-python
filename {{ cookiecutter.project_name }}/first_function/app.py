import boto3
import json
import os

{%- if cookiecutter.include_xray == "y" %}
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all  # Patch all supported libraries for X-Ray - More info: https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-patching.html

# Only instrument libraries if not running locally
if "AWS_SAM_LOCAL" not in os.environ:
    patch_all()
{%- endif %}

# Global variables are reused across execution contexts (if available)
session = boto3.Session()


def lambda_handler(event, context):
    """
        AWS Lambda handler
        Parameters
        ----------
        context: object, required
            Lambda Context runtime methods and attributes

        Attributes
        ----------

        context.aws_request_id: str
            Lambda request ID
        context.client_context: object
            Additional context when invoked through AWS Mobile SDK
        context.function_name: str
            Lambda function name
        context.function_version: str
            Function version identifier
        context.get_remaining_time_in_millis: function
            Time in milliseconds before function times out
        context.identity:
            Cognito identity provider context when invoked through AWS Mobile SDK
        context.invoked_function_arn: str
            Function ARN
        context.log_group_name: str
            Cloudwatch Log group name
        context.log_stream_name: str
            Cloudwatch Log stream name
        context.memory_limit_in_mb: int
            Function memory

            https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

        event: dict, required
        {% if cookiecutter.include_apigw == "y" %}
            API Gateway Lambda Proxy Input Format

            {
                "resource": "Resource path",
                "path": "Path parameter",
                "httpMethod": "Incoming request's method name"
                "headers": {Incoming request headers}
                "queryStringParameters": {query string parameters }
                "pathParameters":  {path parameters}
                "stageVariables": {Applicable stage variables}
                "requestContext": {Request context, including authorizer-returned key-value pairs}
                "body": "A JSON string of the request payload."
                "isBase64Encoded": "A boolean flag to indicate if the applicable request payload is Base64-encode"
            }

            https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
        {% endif %}
        Returns
        ------
        {% if cookiecutter.include_apigw == "y" %}
        API Gateway Lambda Proxy Output Format: dict
            'statusCode' and 'body' are required

            {
                "isBase64Encoded": true | false,
                "statusCode": httpStatusCode,
                "headers": {"headerName": "headerValue", ...},
                "body": "..."
            }

            # api-gateway-simple-proxy-for-lambda-output-format
            https: // docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
        {% endif %}
    """

    message = get_message()
{% if cookiecutter.include_apigw == "y" %}
    return {
        "statusCode": 200,
        "body": json.dumps(message)
    }
{% else %}
    return message
{% endif %}

{% if cookiecutter.include_xray == "y" -%}
# For simple subsegments that don't need annotation/metadata you can use the decorated version
## @xray_recorder.capture('## get_message_subsegment')
{% endif -%}
def get_message():
    {% if cookiecutter.include_xray == "y" -%}
    """
        You can create a sub-segment specifically to a function
        then capture what sub-segment that is inside your code
        and you can add annotations that will be indexed by X-Ray
        for example: put_annotation("operation", "query_db")
    """
    # Only run xray in the AWS Lambda environment
    if "AWS_SAM_LOCAL" not in os.environ:
        xray_subsegment = xray_recorder.current_subsegment()
        xray_subsegment.put_annotation("method", "get_message") # indexed key/value data that X-Ray can use to sort traces by
        
        # Sample metadata - Same as annotation but non-indexed data + allows for objects/dicts
        # subsegment.put_metadata("operation", "metadata", "python object/json")
        xray_recorder.end_subsegment()
    {% endif -%}

    return {"hello": "world"}
