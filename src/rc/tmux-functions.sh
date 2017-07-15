#!/bin/bash

# Returns tmux's version
function _get_tmux_version() {
    tmux -V | cut -c 6-
}

# Returns tmux's major version.
function _get_tmux_major_version() {
    local full_version; full_version="$(_get_tmux_version)"
    local first_dot_index; first_dot_index="$(strindexof "${full_version}" .)"
    
    printf "%s\n" "${full_version:0:${first_dot_index}}"
}

# Returns tmux's minor version.
function _get_tmux_minor_version() {
    local full_version; full_version="$(_get_tmux_version)"
    local first_dot_index; first_dot_index="$(strindexof "${full_version}" .)"
    local second_dot_index; second_dot_index="$(strindexof "${full_version}" . --start=$((first_dot_index + 1)))"
    
    if [[ ${second_dot_index} == "-1" ]]; then
        printf "%s\n" "${full_version:$((first_dot_index + 1))}"
    else
        printf "%s\n" "${full_version:$((first_dot_index + 1)):$((second_dot_index - first_dot_index - 1))}"
    fi
}

# Exit with a status code of zero if tmux's major version is 1.  Otherwise, exits with a non-zero number.
function _is_tmux_v1() {
    [[ "$(_get_tmux_major_version)" == "1" ]]
}

# Exit with a status code of zero if tmux's major version is 2.  Otherwise, exits with a non-zero number.
function _is_tmux_v2() {
    [[ "$(_get_tmux_major_version)" == "2" ]]
}

# Exit with a status code of zero if tmux's has a major version of 2 and a minor version that is greater than or equal
# to 4.  Otherwise, exits with a non-zero number.
function _is_tmux_v2_4p() {
    _is_tmux_v2 && [[ "$(_get_tmux_minor_version)" -ge "4" ]]
}

function _is_tmux_in_cygwin() {
    uname | grep -qi cygwin
}

function _is_tmux_in_linux_with_xclip() {
    uname | grep -qi linux && which xclip > /dev/null
}
