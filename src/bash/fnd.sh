#!/bin/bash

readonly NO_ERR=0
readonly ERR_ARG_COUNT=3

dir=
pattern=
err=${NO_ERR}

if [[ $# == 1 ]]; then
    pattern="$1"
    dir="."
elif [[ $# == 2 ]]; then
    pattern="$1"
    dir="$2"
else
    err=${ERR_ARG_COUNT}
    printf 1>&2 "Invalid number of arguments.\n"
    printf 1>&2 "Correct usage: %s <pattern> [directory]\n" "$(basename $0)"
fi

if [[ ${err} == 0 ]]; then
    find "${dir}" | grep -i --color=auto "${pattern}"
    err=$?
fi

exit ${err}
