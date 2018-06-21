import boto3
import json
import os


def runs_on_aws_lambda():
    """
        Returns True if this function is executed on AWS Lambda service.
    """
    return 'AWS_SAM_LOCAL' not in os.environ and 'LAMBDA_TASK_ROOT' in os.environ

{%- if cookiecutter.include_xray == "y" %}
from aws_xray_sdk.core import xray_recorder

# Patch all supported libraries for X-Ray - More info: https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-patching.html
if runs_on_aws_lambda():
    from aws_xray_sdk.core import patch_all
    patch_all()
{%- endif %}

session = boto3.Session()


def lambda_handler(event, context):
    """
        AWS Lambda handler
        {% if cookiecutter.include_apigw == "y" %}

        This method is invoked by the API Gateway: /Prod/first/{proxy+} endpoint.
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
# Decorator for xray
@xray_recorder.capture('## get_message_segment')
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
    if runs_on_aws_lambda():
        xray_subsegment = xray_recorder.current_subsegment()
        xray_subsegment.put_annotation("key", "value")
    {% endif -%}

    return { "hello": "world" }
