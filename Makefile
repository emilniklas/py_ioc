run ?= app/main.py
install ?= -r requirements.txt

CWD = $(shell pwd)
RUN = docker run \
	--rm \
	--interactive \
	--volume '$(CWD):/app' \
	--workdir '/app' \
	--publish '3000:3000' \
	--env PYTHONPATH=/app/.pip \
	--tty \
	python:latest

.PHONY: run
run:
	$(RUN) $(run)

.PHONY: install
install:
	$(RUN) pip install -t .pip $(install) && \
	$(RUN) pip freeze > requirements.txt

.PHONY: test
test:
	$(RUN) python -m pytest tests/
