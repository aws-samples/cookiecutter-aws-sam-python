import boto3
import json
{%- if cookiecutter.include_xray == "y" %}
from aws_xray_sdk.core import xray_recorder

# Patch all supported libraries for X-Ray - More info: https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-patching.html
if 'LAMBDA_TASK_ROOT' in os.environ:
    from aws_xray_sdk.core import patch_all 
    patch_all()
{%- endif %}

session = boto3.Session()


def lambda_handler(event, context):
{% if cookiecutter.include_apigw == "y" %}
    return {
        "statusCode": 200,
        "body": json.dumps(my_function())
    }
{% else %}
    return my_function()
{% endif %}

{% if cookiecutter.include_xray == "y" -%}
# Decorator for xray
@xray_recorder.capture('## my_function_subsegment')
{% endif -%}
def my_function():
    {% if cookiecutter.include_xray == "y" -%}
    """
        You can create a sub-segment specifically to a function
        then capture what sub-segment that is inside your code
        and you can add annotations that will be indexed by X-Ray
        for example: put_annotation("operation", "query_db")
    """
    # Only run xray in the AWS Lambda environment
    if 'AWS_SAM_LOCAL' not in os.environ and 'LAMBDA_TASK_ROOT' in os.environ:
        xray_subsegment = xray_recorder.current_subsegment()
        xray_subsegment.put_annotation("key", "value")
    {% endif -%}

    return {
        "hello": "world"
    }
