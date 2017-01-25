install ?= -r requirements.txt

CWD = $(shell pwd)
RUN = docker run \
	--rm \
	--interactive \
	--volume '$(CWD):/app' \
	--workdir '/app' \
	--env PYTHONPATH=/app/.pip \
	--tty \
	python:latest

.PHONY: install
install:
	$(RUN) pip install -t .pip $(install) && \
	$(RUN) pip freeze > requirements.txt

.PHONY: test
test:
	$(RUN) python -m pytest tests/
