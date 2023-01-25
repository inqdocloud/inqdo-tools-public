#!/bin/bash

echo "Running docker compose"
cd ../src
docker-compose up -d --build
cd ../scripts
