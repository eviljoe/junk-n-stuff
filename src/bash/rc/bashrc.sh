#!/bin/bash

# ######### #
# Functions #
# ######### #

function add_path {
    local new_path; new_path="$1"
    local place; place="$2"
    local exit_code; exit_code="1"
    
    echo ":${PATH}:" | grep ":${new_path}:" &>/dev/null
    
    if [[ "$?" == "1" ]]; then
        if [[ "${place}" == "start" ]]; then
            export PATH="${new_path}:${PATH}"
        else
            export PATH="${PATH}:${new_path}"
        fi
        
        exit_code="0"
    fi
    
    return "${exit_code}"
}

function print_last_exit_code {
    local exit_code=$?
    
    if [[ "${exit_code}" != "0" ]]; then
        printf "(%d)" "${exit_code}"
    fi
}

function cdh {
    local dir; dir="$1"
    cd "${HOME}/${dir}" || return 1
}

function create_ps1 {
    local ps1; ps1=""
    
    ps1="${ps1}\u"                       # username
    ps1="${ps1}@"                        # at (@)
    ps1="${ps1}\h"                       # host up to fisrt period (.)
    ps1="${ps1}:"                        # colon (:)
    ps1="${ps1}\w"                       # current directory with $HOME as tilda (~)
    ps1="${ps1}\[\e[31m\]"               # make exit code red
    ps1="${ps1}\`print_last_exit_code\`" # last exit code
    ps1="${ps1}\[\e[m\]"                 # clear exit code color
    ps1="${ps1}\$"                       # dollar sign (#).  pound (#) when root
    ps1="${ps1} "                        # space ( )
    
    export PS1="${ps1}"
}

function _can_ls_group_dirs_first {
    ls --group-directories-first &>/dev/null
    return $?
}

# ############## #
# Env. Variables #
# ############## #

create_ps1

add_path ~/bin
add_path ~/.cabal/bin # location of `shellcheck'

export LESSOPEN="|${HOME}/bin/lesspipe %s"

# ####### #
# Aliases #
# ####### #

# cd
alias cd.="cd ."
alias cd..="cd .."
alias cd...="cd ../.."
alias cd....="cd ../../.."
alias cdp='cd $(pwd -P)'
alias desktop="cd ~/Desktop"
alias docs="cd ~/Documents"

# ls
if _can_ls_group_dirs_first; then
    alias ls="ls -hp --color=auto --group-directories-first"
else
    alias ls="ls -hp --color=auto"
fi
alias ll="ls -l"
alias lla="ls -la"
alias ltr="ls -ltr"
alias ltar="ls -ltar"

# Misc.
alias apmu="apm update --no-confirm"
alias cls="tput reset"
alias df="df -h"
alias du="du -h"
alias emacs="emacs -nw"
alias less="less -iRP '?f%f:<stdin>.?m (%i of %m)., %lb of %L (%Pb\\%)'"
alias open="xdg-start"
alias naut="nemo"
alias path='printf "%s\n" "${PATH}"'
alias pwdp='pwd -P'
alias resource="source ~/.bashrc"
alias volume="pavucontrol"

# OS Specific Aliases
_bashrc_os="$(uname -o | tr "[:upper:]" "[:lower:]")"

if [[ "${_bashrc_os}" == "cygwin" ]]; then
    alias open="cygstart"
    alias naut="explorer"
elif [[ "${_bashrc_os}" == "darwin" ]]; then
    alias cls="clear"
    unalias open
    alias naut="open"
fi

# ######## #
# Clean Up #
# ######## #

unset -f _can_ls_group_dirs_first
unset _bashrc_os
