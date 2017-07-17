#!/bin/bash

_is_tmux_v2 && [ "$(_get_tmux_minor_version)" -le "3" ]

