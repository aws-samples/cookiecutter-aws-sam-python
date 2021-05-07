import json

from hello_world import app


def test_lambda_handler(apigw_event, lambda_context):
    ret = app.lambda_handler(apigw_event, lambda_context)
    expected = json.dumps({"message": "hello universe"}, separators=(",", ":"))

    assert ret["statusCode"] == 200
    assert ret["body"] == expected
