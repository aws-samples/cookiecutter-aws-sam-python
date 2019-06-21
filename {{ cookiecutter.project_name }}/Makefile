{% if cookiecutter.include_experimental_make == "y" %}

#########################################################
#														#
# EXPERIMENTAL - Only use if you know what you're doing #
#														#
#########################################################

BASE := $(shell /bin/pwd)
CODE_COVERAGE = 72
PIPENV ?= pipenv

################# 
#  Python vars	#
################# 

SERVICE ?= service_not_defined
EVENT ?= event_not_defined

############# 
#  SAM vars	#
############# 

NETWORK = ""

target:
	$(info ${HELP_MESSAGE})
	@exit 0

clean: ##=> Deletes current build environment and latest build
	$(info [*] Who needs all that anyway? Destroying environment....)
	rm -rf ./${SERVICE}/build
	rm -rf ./${SERVICE}.zip

all: clean build

install: _install_packages _install_dev_packages

shell: 
	@$(PIPENV) shell
	
package: _check_service_definition ##=> Builds package using Docker Lambda container
ifeq ($(DOCKER),1)
	$(info [*] Cleaning up local dev/builds before build task...)
	@$(MAKE) clean SERVICE="${SERVICE}"
	$(info [+] Packaging service '$(SERVICE)' using Docker Lambda -- This may take a while...)
	docker run -v $$PWD:/var/task -it lambci/lambda:build-python3.6 /bin/bash -c 'make _package SERVICE="${SERVICE}"'
else
	$(info [*] Cleaning up local builds before build task...)
	@$(MAKE) clean SERVICE="${SERVICE}"
	$(info [+] Packaging service '$(SERVICE)' -- This may take a while...)
	@$(MAKE) _package SERVICE="${SERVICE}"
endif

build: _check_service_definition _clone_service_to_build ##=> Same as package except that we don't create a ZIP
	@$(MAKE) _install_deps SERVICE="${SERVICE}"

invoke: _check_event_definition ##=> Run SAM Local function with a given event payload
	@sam local invoke ${SERVICE} --event ${EVENT}

run: ##=> Run SAM Local API GW and can optionally run new containers connected to a defined network
	@test -z ${NETWORK} \
		&& sam local start-api \
		|| sam local start-api --docker-network ${NETWORK}

test: ##=> Run pytest
	@AWS_XRAY_CONTEXT_MISSING=LOG_ERROR $(PIPENV) run python -m pytest --cov . --cov-report term-missing --cov-fail-under $(CODE_COVERAGE) tests/ -v

############# 
#  Helpers  #
############# 

_install_packages:
	$(info [*] Install required packages...)
	@$(PIPENV) install

_install_dev_packages:
	$(info [*] Install required dev-packages...)
	@$(PIPENV) install -d

_check_service_definition:
	$(info [*] Checking whether service $(SERVICE) exists...)

# SERVICE="<name_of_service>" must be passed as ARG for target or else fail
ifndef SERVICE
	$(error [!] SERVICE env not defined...FAIL)
endif

ifeq ($(wildcard $(SERVICE)/.),)
	$(error [!] '$(SERVICE)' folder doesn't exist)
endif

ifeq ($(wildcard Pipfile),)
	$(error [!] Pipfile dependencies file missing from $(BASE) folder...)
endif

_check_event_definition:
	$(info [*] Checking whether event $(EVENT) exists...)

# EVENT="<name_and_path_of_event>" must be passed as ARG for target or else fail
ifndef EVENT
	$(error [!] EVENT env not defined...FAIL)
endif

ifeq ($(wildcard $(EVENT)),)
	$(error [!] '$(EVENT)' file doesn't exist)
endif

_clone_service_to_build:
ifeq ($(wildcard $(SERVICE)/build/.),)
	$(info [+] Setting permissions for files under ${SERVICE}/)
	@find ${SERVICE}/ -type f -exec chmod go+r {} \;
	$(info [+] Setting permissions for directories under ${SERVICE}/)
	@find ${SERVICE}/ -type d -exec chmod go+rx {} \;
	$(info [+] Cloning ${SERVICE} directory structure to ${SERVICE}/build)
	@rsync -a -f "+ */" -f "- *" ${SERVICE}/ ${SERVICE}/build/
	$(info [+] Cloning source files from ${SERVICE} to ${SERVICE}/build)
	@find ${SERVICE} -type f \
			-not -name "*.pyc" \
			-not -name "*__pycache__" \
			-not -name "requirements.txt" \
			-not -name "event.json" \
			-not -name "build" | cut -d '/' -f2- > .results.txt
	@while read line; do \
		ln -f ${SERVICE}/$$line ${SERVICE}/build/$$line; \
	done < .results.txt
	@rm -f .results.txt
	$(info [+] Copying events to ${SERVICE}/build)
	@test -d events && rsync -avz events ${SERVICE}/build/
else
	$(info [-] '$(SERVICE)' already has a development build - Ignoring cloning task...)
endif

_check_dev_definition: _check_service_definition
	$(info [*] Checking whether service $(SERVICE) development build exists...)

ifeq ($(wildcard $(SERVICE)/build/.),)
	$(warning [FIX] run 'make build SERVICE=$(SERVICE)' to create one")
	$(error [!] '$(SERVICE)' doesn't have development build)
endif

_install_deps:
	$(info [+] Installing '$(SERVICE)' dependencies...")	
	@pip install pipenv
	@$(PIPENV) lock -r > requirements.txt
	@$(PIPENV) run pip install \
		--isolated \
		--disable-pip-version-check \
		-Ur requirements.txt -t ${SERVICE}/build/
	@rm -f requirements.txt

# Package application and devs together in expected zip from build
_package: _clone_service_to_build _check_service_definition _install_deps
	@$(MAKE) _zip SERVICE="${SERVICE}"

# As its name states: Zip everything up from build
_zip: _check_dev_definition 
	$(info [+] Creating '$(SERVICE)' ZIP...")
	@cd ${SERVICE}/build && zip -rq -9 "$(BASE)/$(SERVICE).zip" * \
	--exclude "wheel/*" "setuptools/*" "pkg_resources/*" "pip/*" \
			  "easy_install.py" "__pycache__/*" "*.dist-info/*" "./**/__pycache__/*"
	$(info [*] Build complete: $(BASE)/$(SERVICE).zip)

define HELP_MESSAGE
	Environment variables to be aware of or to hardcode depending on your use case:

	SERVICE
		Default: not_defined
		Info: Environment variable to declare where source code for lambda is

	DOCKER
		Default: not_defined
		Info: Environment variable to declare whether Docker should be used to build (great for C-deps)

	Common usage:

	...::: Installs all required packages as defined in the pipfile :::...
	$ make install

	...::: Spawn a virtual environment shell :::...
	$ make shell

	...::: Cleans up the environment - Deletes Virtualenv, ZIP builds and Dev env :::...
	$ make clean SERVICE="slack"

	...::: Creates local dev environment for Python hot-reloading w/ packages:::...
	$ make build SERVICE="first_function"

	...::: Bundles app and dependencies into a ZIP file :::...
	$ make package SERVICE="email"

	...::: Bundles app and dependencies into a ZIP file using Docker:::...
	$ make package SERVICE="email" DOCKER=1

	...::: Run SAM Local API Gateway :::...
	$ make run

	...::: Run Pytest under tests/ with pipenv :::...
	$ make test

	Advanced usage:

	...::: Run SAM Local API Gateway within a Docker Network :::...
	$ make run NETWORK="sam-network"
endef

{% endif %}
