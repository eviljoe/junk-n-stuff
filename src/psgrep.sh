#!/bin/bash

readonly NO_ERR=0
readonly ERR_ARG_COUNT=3
readonly ERR_NO_PATTERN=4

pattern=
err=${NO_ERR}

if [[ $# == 1 ]]; then
    pattern="$1"
else
    err=${ERR_ARG_COUNT}
    printf 1>&2 "Invalid number of arguments.\n"
    printf 1>&2 "Correct usage: %s <pattern>\n" "$(basename $0)"
fi

if [[ "${#pattern}" == "0" ]]; then
    err=${ERR_NO_PATTERN}
    printf 1>&2 "The pattern cannot be empty\n"
fi

if [[ ${err} == 0 ]]; then
    ps -ef | grep -i --color=auto "${pattern}"
    err=$?
fi

exit ${err}
