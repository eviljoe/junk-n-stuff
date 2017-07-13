#!/bin/bash
# A script to count the characters of the given words

readonly ERR_NO_ARGS=3


# The main function of the script.
#
# Parameters:
# $1: The command line arguments that were passed to the script
#
# Returns:
# Returns 0 if the function executes successfully.  Returns a non-zero number if an error occurs.
function main() {
    local err=0;
    
    validate_input "$@"
    err=$?
    
    if [[ "${err}" == "0" ]]; then
        if [[ "$#" == "1" ]]; then
            print_char_count "$1" "0"
        else
            for word in "$@"; do
                print_char_count "${word}" "1"
            done
        fi
    fi
    
    return ${err}
}

# Validates the input to the script.
#
# Parameters:
# $1: The command line arguments that were passed to the script
#
# Returns:
# Returns 0 if the input is valid.  Returns a non-zero number if the input is invalid.
function validate_input() {
    local err=0
    
    if [[ "$#" -lt "1" ]]; then
        printf "At least one word must be specified.\n" 1>&2
        printf "Usage: %s <word1> [word2]... \n" "$(basename "$0")" 1>&2
        err=${ERR_NO_ARGS}
    fi
    
    return ${err}
}

# Counts and prints the number of characters in the given word (or phrase).
#
# Parameters:
# $1: The word whose characters are to be counted.
# $2: Whether or not to print word whose characters are to be counted.  If 1, the word will be printed.  Otherwise, the
#     word will not be printed.
function print_char_count() {
    local word; word="$1"
    local print_word; print_word="$2"
    local count; count="$(printf "%s" "${word}" | wc --chars | xargs)"
    
    printf "%s" "${count}"
    
    if [[ "$print_word" == "1" ]]; then
        printf ": %s" "$word"
    fi
    
    printf "\n"
}

main "$@"
