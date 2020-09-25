import json

from hello_world import app


def test_lambda_handler(apigw_event, lambda_context):
    ret = app.lambda_handler(apigw_event, lambda_context)

    assert ret['statusCode'] == 200
    assert ret['body'] == json.dumps({'hello': 'world'})
