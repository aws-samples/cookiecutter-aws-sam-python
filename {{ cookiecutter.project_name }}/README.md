# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Requirements

* AWS CLI with Administrator permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)
* [SAM CLI installed](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

> **NOTE for Windows users**: If you don't have WSL or Make installed, alternative commands to Make are provided in Appendix/Makefile section.

### Local development

Provided that you have requirements above installed, proceed by building the sample Lambda function:

> **NOTE**: Repeat this process upon source code changes.

```bash
make build
```

{% if cookiecutter.include_apigw == "y" %}
**Invoking function locally through local API Gateway**

```bash
make run
```

If the previous command run successfully you should now be able to hit the following local endpoint to invoke your function `http://localhost:3000/first/REPLACE-ME-WITH-ANYTHING`.

**Invoking function locally by passing event as a file**

```bash
sam local invoke FirstFunction -e event.json
```
{% else %}
**Invoking function locally**

```bash
echo '{"message": "Hello" }' | sam local invoke FirstFunction
```
{% endif %}

## Testing

`Pytest` is used to discover tests created under `tests` folder. If you don't have `Pytest` and `Coverage plugin` for Pytest within your Python environment you need to install them before running the test runner:

```bash
make install
```

With development dependencies installed, run our initial unit tests via Pytest runner:

```bash
make test
```

## Packaging and Deployment

AWS Lambda Python runtime requires a flat folder with all dependencies including the application in a ZIP file. 

The build command that we ran in the Local Development section built artifacts that are ready to be packaged as ZIP. SAM CLI does that by reading `CodeUri` property of every function, install dependencies via Pip and copies the source code to the build folder (`.aws-sam/build/FirstFunction/`).

```yaml
...
    FirstFunction:
        Type: AWS::Serverless::Function
        Properties:
            CodeUri: first_function
            ...
```

For packaging, we need a S3 bucket that SAM CLI will use to create and upload a ZIP file with our readily built artifacts.

If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://BUCKET_NAME
```

With your S3 bucket created, run the following command to package our built artifacts to S3:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket BUCKET_NAME
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name {{ cookiecutter.project_name.lower().replace(' ', '-') }} \
    --capabilities CAPABILITY_IAM
```

> **See [Serverless Application Model (SAM) HOWTO Guide](https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md) for more details in how to get started.**

{% if cookiecutter.include_apigw == "y" %}
After deployment is complete you can retrieve the API Gateway Endpoint URL by running:

```bash
aws cloudformation describe-stacks \
    --stack-name {{ cookiecutter.project_name.lower().replace(' ', '-') }} \
    --query 'Stacks[].Outputs'
```
{% endif %}

# Appendix

## Makefile

The sample Makefile provided only works on OSX/Linux but the tasks above can easily be turned into a Powershell or any scripting language you may want it too.

The following make targets will automate that we went through above:

* Find all available targets: **`make`**
* Install Pytest and Pytest plugins: **``make install``**
    - **[Alternative command]**: ``pip install -r requirements-dev.txt``
* Build all Lambda functions available in `template.yaml`: **`make build`**
    - **[Alternative command]**: ``sam build``
* Run `Pytest` against all tests found under `tests` folder: **`make test`**
    - **[Alternative command]**: ``AWS_XRAY_CONTEXT_MISSING=LOG_ERROR pipenv run python -m pytest tests/ -v``
* Build all Lambda functions available in `template.yaml` within Amazon Linux container (useful for Native dependencies/C-bindings) : **`make build DOCKER=1`**
    - **[Alternative command]**: ``sam build --use-container``

## CLI commands

SAM and AWS CLI commands to package, deploy and describe outputs defined within the cloudformation stack:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket BUCKET_NAME

sam deploy \
    --template-file packaged.yaml \
    --stack-name {{ cookiecutter.project_name.lower().replace(' ', '-') }} \
    --capabilities CAPABILITY_IAM

aws cloudformation describe-stacks \
    --stack-name {{ cookiecutter.project_name.lower().replace(' ', '-') }} --query 'Stacks[].Outputs'
```
