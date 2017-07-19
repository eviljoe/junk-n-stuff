#!/bin/bash

full_version="$(_get_tmux_version)"
first_dot_index="$(strindexof "${full_version}" .)"
second_dot_index="$(strindexof "${full_version}" . --start=$((first_dot_index + 1)))"

if [[ ${second_dot_index} == "-1" ]]; then
    printf "%s\n" "${full_version:$((first_dot_index + 1))}"
else
    printf "%s\n" "${full_version:$((first_dot_index + 1)):$((second_dot_index - first_dot_index - 1))}"
fi

