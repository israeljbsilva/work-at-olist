PIP := pip install -r

PROJECT_NAME := work-at-olist
PYTHON_VERSION := 3.6.6
VENV_NAME := $(PROJECT_NAME)-$(PYTHON_VERSION)

# Environment setup
.pip:
	pip install pip --upgrade

setup: .pip
	$(PIP) requirements.txt

.create-venv:
	pyenv install -s $(PYTHON_VERSION)
	pyenv uninstall -f $(VENV_NAME)
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME)
	pyenv local $(VENV_NAME)

create-venv: .create-venv setup

code-convention:
	flake8
	pycodestyle

# Tests
test:
	py.test --cov-report=term-missing  --cov-report=html --cov=.

all: create-venv setup
