import json
import os

import boto3
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver

# https://awslabs.github.io/aws-lambda-powertools-python/#features
tracer = Tracer()
logger = Logger()
metrics = Metrics()
app = ApiGatewayResolver()

# Global variables are reused across execution contexts (if available)
# session = boto3.Session()

@app.get("/hello")
def hello():
    query_string_name = app.current_event.get_query_string_value(name="name", default_value="universe")
    return {"message": f"hello {query_string_name}"}


@app.get("/hello/<name>")
def hello_you(name):
    # query_strings_as_dict = app.current_event.query_string_parameters
    # json_payload = app.current_event.json_body
    return {"message": f"hello {name}"}

@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event, context: LambdaContext):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise
