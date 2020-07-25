import json
import pytest
from .mock import MockContext
from hello_world import app

{% if cookiecutter.include_apigw == "y" %}
@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    with open("./events/hello_world_apigw_event.json", "r") as fp:
        return json.load(fp)

def test_lambda_handler(apigw_event):
    ret = app.lambda_handler(apigw_event, MockContext(__name__))
    assert ret['statusCode'] == 200
    assert ret['body'] == json.dumps({'hello': 'world'})

{% else %}

@pytest.fixture()
def lambda_event():
    """ Generates Lambda Event"""
    with open("./events/hello_world_event.json", "r") as fp:
        return json.load(fp)

def test_lambda_handler(lambda_event):
    ret = app.lambda_handler(lambda_event, MockContext(__name__))
    assert ret == {'hello': 'world'}
{% endif %}
