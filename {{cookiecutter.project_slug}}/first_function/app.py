import boto3
import json
{%- if cookiecutter.include_xray == "y" %}
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all 

# Patch all supported libraries for X-Ray - More info: https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-patching.html
patch_all()
{%- endif %}

session = boto3.Session()


def lambda_handler(event, context):
{% if cookiecutter.include_apigw == "y" %}
    return {
        "statusCode": 200,
        "body": json.dumps({'hello': 'world'})
    }
{% else %}
    return {
        "hello": "world"
    }
{% endif %}

{% if cookiecutter.include_xray == "y" -%}
# Decorator for sync function
@xray_recorder.capture('## my_function_subsegment')
def my_function():
    """
        You can create a sub-segment specifically to a function
        then capture what sub-segment that is inside your code
        and you can add annotations that will be indexed by X-Ray
        for example: put_annotation("operation", "query_db")
    """
    xray_subsegment = xray_recorder.current_subsegment()
    xray_subsegment.put_annotation("key", "value")
    # do something
{% endif -%}
