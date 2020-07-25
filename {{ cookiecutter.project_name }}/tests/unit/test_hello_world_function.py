import json

import pytest
from hello_world import app

from .mock import MockContext


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    with open("./events/hello_world_event.json", "r") as fp:
        return json.load(fp)

def test_lambda_handler(apigw_event):
    ret = app.lambda_handler(apigw_event, MockContext(__name__))
    assert ret['statusCode'] == 200
    assert ret['body'] == json.dumps({'hello': 'world'})
