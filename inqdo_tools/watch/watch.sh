#!/bin/bash

GREEN=`tput setaf 2`
RED=`tput setaf 1`
YELLOW=`tput setaf 3`
CYAN=`tput setaf 6`
C=`tput sgr0`

logger () {
    echo ""
    echo "${GREEN}#############################################${C}"
    echo $1
    echo "${GREEN}#############################################${C}"
    echo ""
}
logger_error () {
    echo ""
    echo "${RED}#############################################${C}"
    echo $1
    echo "${RED}#############################################${C}"
    echo ""
}

CONTAINER=$1
SOURCE=$2

if [ \( -z "$1" \) -o \( -z "$2" \) ]; then
  logger_error "Arguments are missing - CONTAINER NAME - SOURCE"
else
  logger "Watching container: ${CYAN}${CONTAINER}${C}"

  python main.py $CONTAINER $SOURCE
fi  
