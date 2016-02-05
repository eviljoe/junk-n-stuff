#!/bin/bash

# A script to start the murmur server.  In order for the murmur server to be
# able to read the `mumble-server.ini' file, this script needs to be invoked
# with root priviledges.
#
# This script requires the murmur daemon (murmurd).  It is part of the
# "mumble-server" package.

config_file=/etc/mumble-server.ini

if [[ -w "${config_file}" ]]; then
    murmurd -ini "${config_file}"
else
    echo "Cannot start murmur server: Permission denied."
    exit 130
fi
