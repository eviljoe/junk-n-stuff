#!/bin/bash
# A script to fix Cinnamon when it freezes by sending SIGHUP

pkill -HUP -f "cinnamon --replace"
