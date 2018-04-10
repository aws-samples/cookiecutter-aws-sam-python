{% if cookiecutter.include_experimental_make == "y" %}

#########################################################
#														#
# EXPERIMENTAL - Only use if you know what you're doing #
#														#
#########################################################

BASE := $(shell /bin/pwd)

################# 
#  Python vars	#
################# 

SERVICE ?= service_not_defined

############# 
#  SAM vars	#
############# 

NETWORK = ""

target:
	$(info ${HELP_MESSAGE})
	@exit 0

clean: ##=> Deletes current dev environment and latest build
	$(info [*] Who needs all that anyway? Destroying environment....)
	rm -rf ./$(SERVICE)/dev
	rm -rf ./${SERVICE}.zip

all: clean build

package: _check_service_definition ##=> Builds package using Docker Lambda container
ifeq ($(DOCKER),1)
	$(info [*] Cleaning up local dev/builds before build task...)
	@$(MAKE) clean SERVICE="${SERVICE}"
	$(info [+] Packaging service '$(SERVICE)' using Docker Lambda -- This may take a while...)
	docker run -v $$PWD:/var/task -it lambci/lambda:build-python3.6 /bin/bash -c 'make _package SERVICE="${SERVICE}"'
else
	$(info [*] Cleaning up local dev/builds before build task...)
	@$(MAKE) clean SERVICE="${SERVICE}"
	$(info [+] Packaging service '$(SERVICE)' -- This may take a while...)
	@$(MAKE) _package SERVICE="${SERVICE}"
endif

build: _check_service_definition _clone_service_to_dev _install_deps ##=> Same as package except that we don't create a ZIP
	@$(MAKE) _install_deps SERVICE="${SERVICE}"

run: ##=> Run SAM Local API GW and can optionally run new containers connected to a defined network
	@test -z ${NETWORK} \
		&& sam local start-api \
		|| sam local start-api --docker-network ${NETWORK}

test: ##=> Run pytest
	@pipenv run python -m pytest tests/ -v

############# 
#  Helpers	#
############# 

_check_service_definition:
	$(info [*] Checking whether service $(SERVICE) exists...)

# SERVICE="<name_of_service>" must be passed as ARG for target or else fail
ifndef SERVICE
	$(error [!] SERVICE env not defined...FAIL)
endif

ifeq ($(wildcard $(SERVICE)/.),)
	$(error [!] '$(SERVICE)' folder doesn't exist)
endif

ifeq ($(wildcard requirements.txt),)
	$(error [!] Pip requirements file missing from $(BASE) folder...)
endif

_clone_service_to_dev:
	$(info [+] Cloning ${SERVICE} directory structure to ${SERVICE}/dev)
	@rsync -a -f "+ */" -f "- *" -f "- dev/" ${SERVICE}/ ${SERVICE}/dev/
	$(info [+] Cloning source files from ${SERVICE} to ${SERVICE}/dev)
	@find ${SERVICE} -type f \
			-not -name "*.pyc" \
			-not -name "*__pycache__" \
			-not -name "requirements.txt" \
			-not -name "event.json" \
			-not -name "dev" | cut -d '/' -f2- > .results.txt
	@while read line; do \
		ln -f ${SERVICE}/$$line ${SERVICE}/dev/$$line; \
	done < .results.txt
	rm -f .results.txt

_check_dev_definition: _check_service_definition
	$(info [*] Checking whether service $(SERVICE) development build exists...)

ifeq ($(wildcard $(SERVICE)/dev/.),)
	$(warning [FIX] run 'make build-dev SERVICE=$(SERVICE)' to create one")
	$(error [!] '$(SERVICE)' doesn't have development build)
endif

_install_deps:
	$(info [+] Installing '$(SERVICE)' dependencies...")	
	@pip install pipenv
	@pipenv lock -r > requirements.txt
	@pipenv run pip install \
		--isolated \
		--disable-pip-version-check \
		-Ur requirements.txt -t ${SERVICE}/dev/

# Package application and devs together in expected zip from dev
_package: _clone_service_to_dev _check_service_definition _install_deps
	@$(MAKE) _zip SERVICE="${SERVICE}"

# As its name states: Zip everything up from dev
_zip: _check_dev_definition 
	$(info [+] Creating '$(SERVICE)' ZIP...")
	@cd ${SERVICE}/dev && zip -rq -9 "$(BASE)/$(SERVICE).zip" * \
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
