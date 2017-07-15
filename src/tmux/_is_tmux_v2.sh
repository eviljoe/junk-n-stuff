#!/bin/bash

[ "$(_get_tmux_major_version)" -eq "2" ]

# JOE tb
exit_code=$?
echo "value: ${exit_code}" > /home/joe/tmp2.txt
exit ${exit_code}
# JOE eb
