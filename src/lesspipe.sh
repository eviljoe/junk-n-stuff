#!/bin/bash

# `less' can use this file to modify the text that will be displayed when reading a file.  In practice, this allows less
# to display user-readable text for binary files.
#
# To configure less to use this file add the following env. variable:
#
#   LESSOPEN="|/path/to/lesspipe.sh %s"
#    (1)     (2)     (3)            (4)
#
# (1) The name of the env. variable is "LESSOPEN"
# (2) The variable's value needs to start with a pipe (|) character.
# (3) The path to this script
# (4) When less invokes this script, it will put the name of the file in place of this token.

function read_java_archive() {
    local file; file="$1"
    
    printf "/* *********** */\n/* MANIFEST.MF */\n/* *********** */\n\n"
    unzip -p "${file}" "META-INF/MANIFEST.MF" 2>/dev/null
    
    printf "/* ***** */\n/* FILES */\n/* ***** */\n\n"
    jar tvf "${file}" 2>/dev/null
}

case "$1" in
    # TAR + Compression
    *.tar)     tar tvf "$1" 2>/dev/null               ;;
    *.tar.bz2) bzip2 -dc "$1" | tar tvf - 2>/dev/null ;;
    *.tar.gz)  gzip -dc "$1" | tar tvf - 2>/dev/null  ;;
    *.gz)      gzip -lv "$1" 2>/dev/null              ;;
    
    # ZIP
    *.Z)   uncompress -c "$1"  2>/dev/null ;;
    *.zip) unzip -v $1 2>/dev/null         ;;
    
    # Java
    *.ear)   read_java_archive "$1" ;;
    *.jar)   read_java_archive "$1" ;;
    *.war)   read_java_archive "$1" ;;
    *.class) javap -verbose -private -sysinfo -constants "$1" ;;
    
    # ASAR
    *.asar) asar list "$1" ;;
    
    # FLAC
    *.flac) metaflac --list "$1" 2>/dev/null ;;
esac