# InQdo Tools Public

[![CI](https://github.com/inqdocloud/inqdo-tools-public/actions/workflows/ci.yml/badge.svg)](https://github.com/inqdocloud/inqdo-tools-public/actions/workflows/ci.yml)

To develop with this package, Docker is required. The following instructions will guide you on how to build the container, test, and perform linting and documentation tasks.

## Building the container
To build the test environment and run the container in the background, run:

```sh
$ docker-compose up -d --build
```

Alternatively, you can use the script: `exec-build.sh` located in the root directory. 


## Testing
We are using `pytest` for testing the methods.
The library `moto` is used for mocking aws infrastructure [https://docs.getmoto.org/](https://docs.getmoto.org/)


#### Unit tests
To test the methods you can use `pytest`.

```sh
$ docker-compose exec inqdo-tools pytest
```

Alternatively, you can use the script: `exec-pytest.sh` located in the root directory. 

#### Code coverage report
To get a code coverage report you can use this commands:

```sh
$ docker-compose exec inqdo-tools pytest --cov=.
$ ## With HTML report
$ docker-compose exec inqdo-tools pytest --cov=. --cov-report html
$ open tests/htmlcov/index.html
```

Alternatively, you can use the script: `exec-code-coverage.sh` located in the root directory.


## Lint

To run flake8:

```sh
$ # Run flake8
$ docker-compose exec inqdo-tools flake8
```

To run black to automatically format code:

```sh
$ # Run black to automatically format code
$ docker-compose exec inqdo-tools black .
```

To sort Python imports:

```sh
$ # Sort Python imports
$ docker-compose exec inqdo-tools isort .
```

Alternatively, you can use the script: `exec-lint.sh` located in the root directory.

### Local development

For local development, you can launch `Dockerfile-inqdo_tools` via `docker-compose-yml` in the src directory at `inqdo_tools/src/docker-compose.yml`.

You can easliy run script `run.sh` in `inqdo_tools/src/scripts`.

Use the script `invoke-lambda.sh` located in the same direcory as `run.sh` to invoke the Ddocker container.
This scripts expects a parameter (port)

Example: `. invoke-lambda.sh 9000`

`inqdo_tools/src/inqdo_tools/main.py` will be invoked. Use this file for testing your code.


## Docs
To generate the documentation, run:

```sh
$ # Auto generate rst files for the docs. The last argument is for ignoring the debug.py file from the docs
$ docker-compose exec inqdo-tools sphinx-apidoc -f -o docs/source inqdo_tools inqdo_tools/debug.py
$ # Build the documentation
$ docker-compose exec inqdo-tools make html
$ # Open the docs
$ open docs/build/html/index.html
```

Alternatively, you can use the script: `exec-build-docs.sh` located in the root directory.


### Test Github Actions Localy
To test Github Actions locally, you can use the tool `act` found at: [https://github.com/nektos/act](https://github.com/nektos/act)

 However, `act` does not natively support the `docker-compose` command. To overcome this, you can use the custom image : [https://github.com/lucasctrl/act_base](https://github.com/lucasctrl/act_base)

To run this image, use the command:
```sh
$ act pull_request -P ubuntu-latest=lucasalt/act_base:latest
```


### Install
To install inQdo Tools locally, run the following command in your terminal:

```sh
$ pip install "git+https://github.com/inqdocloud/inqdo-tools-public.git@v1.0.0#egg=inqdo-tools&subdirectory=inqdo_tools/src"
```

This command will install the inQdo Tools package from the specified git repository and version (v1.0.0) into your local environment.
