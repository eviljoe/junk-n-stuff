#!/bin/bash
# A script to `git rebase' on `master'

set -euo pipefail

readonly BOLD="\e[1m"
readonly CYAN="\e[36m"
readonly PLAIN="\e[0m"

branch_name=""
err=0

if [[ "$(git status --short | wc -l)" -gt "0" ]]; then
    printf 1>&2 "cannot continue because there are uncommitted changes\n"
    err=1
fi

if [[ "${err}" == "0" ]]; then
    if [[ "$#" == "0" ]]; then
        branch_name="$(git rev-parse --abbrev-ref HEAD)"
    elif [[ "$#" == "1" ]]; then
        branch_name="${1}"
    else
        printf 1>&2 "must either specify branch or use current branch\n"
        err=1
    fi
fi

if [[ "${err}" == "0" && "${branch_name}" == "master" ]]; then
    printf 1>&2 "cannot rebase master on master\n"
    err=1
fi

if [[ "${err}" == "0" ]]; then
    printf "${BOLD}${CYAN}git checkout master${PLAIN}\n"
    git checkout master

    printf "${BOLD}${CYAN}git pull${PLAIN}\n"
    git pull

    printf "${BOLD}${CYAN}git checkout %s${PLAIN}\n" "${branch_name}"
    git checkout "${branch_name}"

    printf "${BOLD}${CYAN}git rebase --interactive master${PLAIN}\n"
    git rebase --interactive master
fi

exit ${err}
