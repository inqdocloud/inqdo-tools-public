#!/usr/bin/env bash

GREEN=`tput setaf 2`
RED=`tput setaf 1`
YELLOW=`tput setaf 3`
CYAN=`tput setaf 6`
C=`tput sgr0`

logger_ok () {
    echo ""
    echo "${GREEN}#############################################${C}"
    echo $1
    echo "${GREEN}#############################################${C}"
    echo ""
}

logger_notok () {
    echo ""
    echo "${RED}#############################################${C}"
    echo $1
    echo "${RED}#############################################${C}"
    echo ""
}

if [[ $# -ge 1 ]]; then
    ACTION=$1

    if [ $ACTION == "html" ]; then
      logger_ok  "${CYAN}Action = $ACTION ${C}"

      docker-compose exec inqdo-tools pytest --cov-config=.coveragerc --cov=. --cov-report html
      open tests/htmlcov/index.html
    else
      logger_notok "Provide argument ${YELLOW}html${C}${RED}, for determine the report${C}"
    fi

else
    docker-compose exec -T inqdo-tools pytest --cov-fail-under=50 --cov=.
fi

