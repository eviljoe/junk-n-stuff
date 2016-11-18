#!/bin/bash

readonly VERSION=1.0.0
readonly ASCII_HOME="${HOME}/.random-ascii"

readonly ACTION_ADD="ADD"
readonly ACTION_DISPLAY_RANDOM="DISPLAY_RANDOM"
readonly ACTION_DISPLAY_SPECIFIED="DISPLAY_SPECIFIED"
readonly ACTION_LIST="LIST"
readonly ACTION_REMOVE="REMOVE"

readonly ERR_INVALID_OPT=2
readonly ERR_OPT_REQUIRES_ARG=3
readonly ERR_ADD_TARGET_DNE=4
readonly ERR_DISPLAY_TARGET_DNE=5
readonly ERR_REMOVE_TARGET_DNE=6

opt_action="${ACTION_DISPLAY_RANDOM}"
opt_action_target=""
opt_print_help=0

function main {
    local err; err=0
    
    parse_opts "$@"
    err=$?
    
    validate_opts "${err}"
    err=$?
    
    if [[ "${err}" == 0 ]]; then
        if [[ "${opt_print_help}" == 1 ]]; then
            print_help
        else
            perform_action
            err=$?
        fi
    fi
    
    return "${err}"
}

function parse_opts {
    local err; err=0
    
    while getopts ":a:Dd:hlr:" opt; do
        case $opt in
            a) opt_action="${ACTION_ADD}"; opt_action_target="${OPTARG}" ;;
            D) opt_action="${ACTION_DISPLAY_RANDOM}" ;;
            d) opt_action="${ACTION_DISPLAY_SPECIFIED}"; opt_action_target="${OPTARG}" ;;
            h) opt_print_help=1 ;;
            l) opt_action="${ACTION_LIST}" ;;
            r) opt_action="${ACTION_REMOVE}"; opt_action_target="${OPTARG}" ;;
            \?)
                printf "Invalid option: -%s\n" "${OPTARG}" 1>&2
                err=${ERR_INVALID_OPT}
                ;;
            :)
                printf "Option -%s requires an argument.\n" "${OPTARG}" 1>&2
                err=${ERR_OPT_REQUIRES_ARG}
                ;;
        esac
    done
    
    return ${err}
}

function print_help {
    local base_name; base_name="$(basename "$0")"
    
    fold -w "$(tput cols)" <<EOF
${base_name}: A script to display some random ASCII
Version: ${VERSION}

Usage: ${base_name} [options]
Options:
  -a <file>: Add a new ASCII file
  -D: Display a random ASCII file
  -d <file>: Display the specified ASCII file
  -h: Print this help message and exit
  -l: List the availble ASCII files
  -r <file>: Remove the specified ASCII file

Examples:
  * To display a random ASCII file: ${base_name}
  * To add a new ASCII file: ${base_name} -a ~/ascii.txt

Notes:
  * If multiple actions are specified, the last one specified will be performed.
EOF
}

function validate_opts {
    local err; err=$1
    
    if [[ "${err}" == 0 ]]; then
        if [[ "${opt_action}" == "${ACTION_ADD}" && ! -f "${opt_action_target}" ]]; then
            printf "The file to add does not exist or is not a regular file.\n" 1>&2
            err="${ERR_ADD_TARGET_DNE}"
        elif [[ "${opt_action}" == "${ACTION_DISPLAY_SPECIFIED}" && ! -f "${ASCII_HOME}/${opt_action_target}" ]]; then
            printf "The file to be displayed does not exist.\n" 1>&2
            err="${ERR_DISPLAY_TARGET_DNE}"
        elif [[ "${opt_action}" == "${ACTION_REMOVE}" && ! -f "${ASCII_HOME}/${opt_action_target}" ]]; then
            printf "The file to be removed does not exist.\n" 1>&2
            err="${ERR_REMOVE_TARGET_DNE}"
        fi
    fi
    
    if [[ "${err}" != "0" ]]; then
        printf "For correct usage, execute: %s -h\n" "$(basename $0)" 1>&2
    fi
    
    return "${err}"
}

function perform_action {
    if [[ "${opt_action}" == "${ACTION_ADD}" ]]; then
        perform_action_add
    elif [[ "${opt_action}" == "${ACTION_DISPLAY_RANDOM}" ]]; then
        perform_action_display_random
    elif [[ "${opt_action}" == "${ACTION_DISPLAY_SPECIFIED}" ]]; then
        perform_action_display_specified
    elif [[ "${opt_action}" == "${ACTION_LIST}" ]]; then
        perform_action_list
    elif [[ "${opt_action}" == "${ACTION_REMOVE}" ]]; then
        perform_action_remove
    fi
}

function perform_action_add {
    cp "${opt_action_target}" "${ASCII_HOME}/$(basename "${opt_action_target}")"
}

function perform_action_display_random {
    local file; file="$(ls -1 "${ASCII_HOME}" | shuf -n 1)"
    
    if [[ -n "${file}" ]]; then
        cat "${ASCII_HOME}/${file}"
    fi
}

function perform_action_display_specified {
    cat "${ASCII_HOME}/${opt_action_target}"
}

function perform_action_list {
    ls -1 "${ASCII_HOME}"
}

function perform_action_remove {
    rm "${ASCII_HOME}/${opt_action_target}"
}

main "$@"
