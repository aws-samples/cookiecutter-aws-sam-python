import json

from hello_world import app


def test_lambda_handler_hello_path(apigw_hello_event, lambda_context):
    ret = app.lambda_handler(apigw_hello_event, lambda_context)
    expected = json.dumps({"message": "hello unknown!"}, separators=(",", ":"))

    assert ret["statusCode"] == 200
    assert ret["body"] == expected


def test_lambda_handler_hello_you_path(apigw_hello_name_event, lambda_context):
    ret = app.lambda_handler(apigw_hello_name_event, lambda_context)
    expected = json.dumps({"message": "hello you!"}, separators=(",", ":"))

    assert ret["statusCode"] == 200
    assert ret["body"] == expected
