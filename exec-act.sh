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

    logger_ok  "ACT ON: ${CYAN}Action = $ACTION ${C}"

    act $ACTION -P ubuntu-latest=lucasalt/act_base:latest

else
    logger_notok "Provide ${YELLOW}action${C}${RED}, for determine the act on action${C}"
fi

