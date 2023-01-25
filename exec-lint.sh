# Run flake8
docker-compose exec inqdo-tools flake8
# Run black to automatically format code
docker-compose exec inqdo-tools black .
# Sort Python imports
docker-compose exec inqdo-tools isort .
