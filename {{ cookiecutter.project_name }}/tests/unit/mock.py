from uuid import uuid4

class MockContext(object):

    def __init__(self, function_name):
        self.function_name = function_name
        self.function_version = "v$LATEST"
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = f"arn:aws:lambda:us-east-1:ACCOUNT:function:{self.function_name}"
        self.aws_request_id = str(uuid4)
