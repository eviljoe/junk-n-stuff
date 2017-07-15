#!/bin/bash

[ "$(_get_tmux_major_version)" -eq "1" ]

# JOE tb
exit_code=$?
echo "value: ${exit_code}" > /home/joe/tmp1.txt
exit ${exit_code}
# JOE eb
