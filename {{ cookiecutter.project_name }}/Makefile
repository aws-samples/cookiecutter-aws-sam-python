
##############################################
#											 #
# SAMPLE - Makefile to abstract common tasks #
#											 #
##############################################

CODE_COVERAGE = 72

############# 
# SAM vars	#
############# 

NETWORK = ""

target:
	$(info ${HELP_MESSAGE})
	@exit 0

clean: ##=> Deletes latest build
	$(info [*] Who needs all that anyway? Destroying artifacts....)
	rm -rf ./.aws-sam/

all: clean build

install: _install_dev_packages

build: ##=> Generates build artifacts for local development/deployment
ifeq ($(DOCKER),1)
	$(info [+] Building all functions available in template.yaml using Docker Lambda -- This may take a while...)
	sam build --use-container
else
	$(info [+] Building all functions available in template.yaml -- This may take a while...)
	sam build
endif

run: ##=> Run SAM Local API GW and can optionally run new containers connected to a defined network
	$(info [+] Starting Local API Gateway service)
	@test -z ${NETWORK} \
		&& sam local start-api \
		|| sam local start-api --docker-network ${NETWORK}

test: ##=> Run pytest
	$(info [+] Starting test runner (pytest))
	@AWS_XRAY_CONTEXT_MISSING=LOG_ERROR python -m pytest --cov . --cov-report term-missing --cov-fail-under $(CODE_COVERAGE) tests/ -v

############# 
#  Helpers  #
############# 

_install_dev_packages:
	$(info [*] Installing development dependencies used for testing...)
	pip install -r requirements-dev.txt

define HELP_MESSAGE
	Environment variables to be aware of or to hardcode depending on your use case:

	DOCKER
		Default: not_defined
		Info: Environment variable to declare whether Docker should be used to build (great for C-deps)

	Common usage:

	...::: Installs development packages required for testing :::...
	$ make install

	...::: Generates build artifacts for local development/deployment :::...
	$ make build

	...::: Generates build artifacts for local development/deployment using a Docker container :::...
	$ make build DOCKER=1

	...::: Run SAM Local API Gateway :::...
	$ make run

	...::: Run Pytest under tests/ with pipenv :::...
	$ make test

	...::: Cleans up the environment - Deletes locally built artifacts from all functions :::...
	$ make clean

	Advanced usage:

	...::: Run SAM Local API Gateway within a Docker Network :::...
	$ make run NETWORK="sam-network"
endef
