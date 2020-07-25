# Cookiecutter SAM for Python Lambda functions

This is a [Cookiecutter](https://github.com/audreyr/cookiecutter) template to create a Serverless App based on Serverless Application Model (SAM) and Python 3.8.

It is important to note that you should not try to `git clone` this project but use `SAM` CLI instead as ``{{cookiecutter.project_slug}}`` will be rendered based on your input and therefore all variables and files will be rendered properly.

## Usage

Generate a new SAM based Serverless App: `sam init --location gh:aws-samples/cookiecutter-aws-sam-python`

You'll be prompted a few questions to help this cookiecutter template to scaffold this project and after its completed you should see a new folder at your current path with the name of the project you gave as input.

## Options

Option | Description
------------------------------------------------- | ---------------------------------------------------------------------------------
`include_safe_deployment` | Sends by default 10% of traffic for every 1 minute to a newly deployed function using [CodeDeploy + SAM integration](https://github.com/awslabs/serverless-application-model/blob/master/docs/safe_lambda_deployments.rst) - Linear10PercentEvery1Minute

# Credits

* This project has been generated with [Cookiecutter](https://github.com/audreyr/cookiecutter)
* [Bruno Alla's Lambda function template](https://github.com/browniebroke/cookiecutter-lambda-function)

License
-------

This project is licensed under the terms of the [MIT License with no attribution](/LICENSE)
