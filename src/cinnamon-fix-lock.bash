#!/bin/bash
# A script to fix the Cinnamon lockscreen/screensaver when it freezes by sending SIGHUP

pkill -HUP -f "cinnamon-screensaver"
