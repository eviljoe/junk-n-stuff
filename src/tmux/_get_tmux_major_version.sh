#!/bin/bash

full_version="$(_get_tmux_version)"
first_dot_index="$(strindexof "${full_version}" .)"

printf "%s\n" "${full_version:0:${first_dot_index}}"
