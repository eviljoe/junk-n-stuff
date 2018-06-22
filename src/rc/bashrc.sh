#!/bin/bash

_bashrc_os="$(uname -o | tr "[:upper:]" "[:lower:]")"

# ######### #
# Functions #
# ######### #

function path {
    printf "%s\n" "${PATH}" | sed "s/:/\n/g"
}

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

function _print_git_branch {
    git rev-parse --abbrev-ref HEAD
}

function cdh {
    local dir; dir="$1"
    cd "${HOME}/${dir}" || return 1
}

function str_lower {
    printf "%s" "$1" | tr "[:upper:]" "[:lower:]"
}

function _is_interactive {
    local interactive;

    case "$-" in
        *i*) interactive=0 ;;
        *) interactive=1 ;;
    esac

    return ${interactive}
}


# this algorithm is from here: http://unix.stackexchange.com/a/9607
function _is_in_ssh {
    local in_ssh; in_ssh=1

    if [[ -n "${SSH_CLIENT}" ]] || [[ -n "${SSH_TTY}" ]]; then
        in_ssh=0
    # The `-o' option isn't supported in Cygwin's `ps' command, so don't check this when in Cygwin.
    elif [[ "$(str_lower "$(uname -o)")" != "cygwin" ]]; then
        case $(ps -o comm= -p $PPID) in
            sshd|*/sshd) in_ssh=0
        esac
    fi

    return ${in_ssh}
}

function _is_in_sudo {
    local in_sudo; in_sudo=1

    if [ -n "${SUDO_COMMAND}" ]; then
        in_sudo=0
    fi

    return ${in_sudo}
}

function _is_in_git_repo {
    which git &>/dev/null && git rev-parse --is-inside-work-tree &>/dev/null
}

function _create_ps1 {
    local last_exit_code=$?
    local ps1

    if _is_in_sudo; then
        ps1="${ps1}\[\e[32m\]" # make username green
        ps1="${ps1}\u"         # username
        ps1="${ps1}\[\e[m\]"   # clear username color
    else
        ps1="${ps1}\u" # username
    fi

    ps1="${ps1}@" # at (@)

    if _is_in_ssh; then
        ps1="${ps1}\[\e[32m\]" # make host green
        ps1="${ps1}\h"         # host up to fisrt period (.)
        ps1="${ps1}\[\e[m\]"   # clear host color
    else
        ps1="${ps1}\h" # host up to fisrt period (.)
    fi

    if _is_in_git_repo; then
        ps1="${ps1}\[\e[92m\]"            # make git branch green
        ps1="${ps1}@$(_print_git_branch)" # print git branch
        ps1="${ps1}\[\e[m\]"              # clear git branch color
    fi

    if [[ "${PIPENV_ACTIVE}" == "1" ]]; then
        ps1="${ps1}\[\e[95m\]" # make pipenv indicator light magenta
        ps1="${ps1}(PE)"       # print pipenv indicator
        ps1="${ps1}\[\e[m\]"   # clear pipenv indicator color
    fi

    ps1="${ps1}:"  # colon (:)
    ps1="${ps1}\w" # current directory with $HOME as tilda (~)

    if [ "${last_exit_code}" -ne "0" ]; then
        ps1="${ps1}\[\e[31m\]"          # make exit code red
        ps1="${ps1}(${last_exit_code})" # print last exit code
        ps1="${ps1}\[\e[m\]"            # clear exit code color
    fi

    ps1="${ps1}\$" # dollar sign ($).  pound (#) when root
    ps1="${ps1} "  # space ( )

    export PS1="${ps1}"
}

function llwhich {
    ll "$(which "$@")"
}

function cdwhich {
    cd "$(dirname "$(which "$@")")" || return 1
}

function _can_ls_group_dirs_first {
    ls --group-directories-first &>/dev/null
    return $?
}

function _start_tmux {
    if [[ -z "${TMUX}" ]] && _is_interactive && type tmux &> /dev/null; then
        tmux
    fi
}

# This only works in Cygwin
if [[ "${_bashrc_os}" == "cygwin" ]]; then
    function which {
        (alias; declare -f) | /usr/bin/which --tty-only --read-alias --read-functions --show-tilde --show-dot "$@"
    }
fi

# ############# #
# Shell Options #
# ############# #

shopt -s checkwinsize # Update window size after every command
shopt -s histappend # Append to the history file, don't overwrite it
shopt -s cdspell 2> /dev/null # Correct spelling errors in arguments supplied to cd

if [[ "${BASH_VERSION:0:1}" -gt "3" ]]; then
    shopt -s dirspell # Correct spelling errors during tab-completion
fi

# ############## #
# Env. Variables #
# ############## #

add_path ~/bin
add_path ~/bin/lib
add_path ~/bin/local
add_path ~/.cabal/bin # location of `shellcheck'

export PROMPT_COMMAND=_create_ps1
export LESSOPEN="|${HOME}/bin/lesspipe %s"
export HISTCONTROL="ignoreboth" # Ignore adjacent duplicate lines and lines that start with a space

# ####### #
# Aliases #
# ####### #

# cd
alias cd.="cd ."
alias cd..="cd .."
alias cd...="cd ../.."
alias cd....="cd ../../.."
alias cd-="cd -"
alias cdp='cd "$(pwd -P)"'
alias cdp..='cd "$(dirname "$(pwd -P)")"'
alias desktop="cd ~/Desktop"
alias docs="cd ~/Documents"

# git
alias gcpp="gitcommitpp"
alias gdiff="git difftool --dir-diff"
alias gdiffs="git difftool --dir-diff --staged"
alias gl1="gitlog1"

# less
alias less="less -iRP '?f%f:<stdin>.?m (%i of %m)., %lb of %L (%Pb\\%)'"
alias les="less -S"
alias lgs="less +G -S"

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
alias disband="ununite"
alias du="du -h"
alias emacs="emacs -nw"
alias grep="grep --color=auto"
alias naut="nemo"
alias open="xdg-open"
alias pwdp='pwd -P'
alias resource="source ~/.bashrc"
alias tree="tree -C"
alias volume="pavucontrol"
alias winch="kill -SIGWINCH \$\$"

# OS Specific Aliases
if [[ "${_bashrc_os}" == "cygwin" ]]; then
    alias open="cygstart"
    alias naut="explorer"
elif [[ "${_bashrc_os}" == "darwin" ]]; then
    alias cls="clear"
    unalias open
    alias naut="open"
fi

# Terminal Emulator Specific Aliases

# When the `TERM' env. var. is `xterm' we are either in Linux or in Cygwin+Mintty.  When the `TERM' env. var. is
# `cygwin' we are in Cygwin but using a terminal emulator other thatn Mintty (e.g. ConsoleZ).
if [[ "$(str_lower "${TERM}")" == "cygwin" ]]; then
    alias cls="tput reset && echo"
fi

# When in tmux, `tput reset' acts like `clear'.
if [[ -n "${TMUX}" ]]; then
    alias cls="tput reset && tmux clear-history"
fi

# ######## #
# Clean Up #
# ######## #

unset -f _can_ls_group_dirs_first
unset _bashrc_os
