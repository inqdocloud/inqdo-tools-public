# docker-compose exec inqdo-tools pytest --cov=.
## With HTML report
docker-compose exec inqdo-tools pytest --cov-config=.coveragerc --cov=. --cov-report html
open tests/htmlcov/index.html
