#!/usr/bin/env bash

# Auto generate rst files for the docs. The last argument is for ignoring the debug.py file from the docs
# docker-compose exec inqdo-tools sphinx-apidoc -f -o docs/source inqdo_tools inqdo_tools/debug.py
docker-compose exec -T inqdo-tools sphinx-apidoc -f -o docs/source inqdo_tools inqdo_tools/debug.py
# Build the documentation
# docker-compose exec inqdo-tools make html
docker-compose exec -T inqdo-tools make html
# Open the docs
open docs/build/html/index.html
