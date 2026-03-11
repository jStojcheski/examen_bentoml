# exam BentoML - STOJCHESKI

![Python](https://img.shields.io/badge/Python-3.12-blue)

## Setup

First, install `uv` by following the [official guideline](https://docs.astral.sh/uv/getting-started/installation/). Then, create a virtual environment by running `uv venv --python 3.12`, activate the environment by running `source .venv/bin/activate`, and install the packages by running `uv sync`. For development and running the tests defined in the `tests/test_api.py` file, install the `dev` dependency group by running `uv sync --group dev`.

## Usage

There is a Docker image saved at `docker/bentoml_stojcheski`. To load this image, run `make docker-load-image`. To start the app, run `make docker-up`.

If you don't want to use the expored Docker image... To start the app, run `make up`. To run the app in dev mode (restart after every saved code change), run `make up-dev`.

## Demo

- Run `make api-login-admin` to get access token that is valid for 24 hours or `make api-login-user` to get access token that is valid for 30 minutes.
- Save the access token as environment variable by running `export ACCESS_TOKEN=<token-value>`
- Run `make train-model` to train a model.
- Run `make api-predict` to get a prediction for an example input.

## Running tests

First, make sure that you have installed the `dev` group of dependencies and that the app is up and running (`make up`). Then, open another terminal, and run `python3 -m pytest -svv tests/` or `make test-api`.
