#!/bin/bash

set -e # fail on any errors

readonly DEF_GIT_HOME="${HOME}/Documents/git"
readonly CLONE_REPO_URL="https://github.com/eviljoe/junk-n-stuff.git"
readonly HOME_BIN_DIR="${HOME}/bin"

readonly ERR_INVALID_OPT=3
readonly ERR_OPT_REQUIRES_ARG=4
readonly ERR_GIT_HOME_NOT_DIR=5

opt_clone_repo=0
opt_print_help=0
opt_dry_run=0
opt_git_home="${DEF_GIT_HOME}"

function main() {
    local err; err=0
    
    parse_opts "$@"
    err=$?
    
    if [[ "${err}" == "0" ]]; then
        if [[ "${opt_print_help}" == "1" ]]; then
            print_help "$@"
        else
            if [[ "${opt_clone_repo}" == "1" ]]; then
                clone_repo
            fi
            
            make_home_bin_dir
            make_bashrc
            make_symbolic_links
        fi
    fi
}

function parse_opts() {
    local err; err=0
    
    while getopts ":cdhg:" opt; do
        case $opt in
            c) opt_clone_repo=1 ;;
            d) opt_dry_run=1 ;;
            h) opt_print_help=1 ;;
            g) opt_git_home="${OPTARG}" ;;
            \?)
                
                printf "Invalid option: -%s\n" "${OPTARG}" 1>&2
                err=${ERR_INVALID_OPT}
                ;;
            :)
                printf "Option -%s requires an argument.\n" "${OPTARG}" 1>&2
                err=${ERR_OPT_REQUIRES_ARG}
                ;;
        esac
    done
    
    if [[ "${err}" != "0" ]]; then
        printf "For correct usage, execute: %s -h\n" "$(basename $0)" 1>&2
    fi
    
    return ${err}
}

function print_help() {
    local base_name; base_name="$(basename "$0")"
    
    cat <<EOF
${base_name}: A script to init junk-n-stuff
Version: ${VERSION}

Usage: ${base_name} [options]
Options:
  -c: Clone repo junk-n-stuff repo
  -d: Do a dry run.  Do not actually perform any actions.
  -g: Git home directory. (default: ${DEF_GIT_HOME})
  -h: Print this help message and exit

Examples:
  To init junk-n-stuff: ${base_name}
  To perform a dry run: ${base_name} -d
EOF
}

function exec_cmd() {
    local cmd
    
    for arg in "$@"; do
        if [[ -z "${cmd}" ]]; then
            cmd="${arg}"
        else
            case "${arg}" in
                *\ *) cmd=$(printf "%s \"%s\"" "${cmd}" "${arg}") ;;
                *) cmd="${cmd} ${arg}" ;;
            esac
        fi
    done
    
    printf "%s\n" "${cmd}"
    
    if [[ "${opt_dry_run}" == 0 ]]; then
        ${cmd}
    fi
}

function clone_repo() {
    local err; err=0;
    
    if [[ ! -e "${opt_git_home}" ]]; then
        exec_cmd mkdir -p "${opt_git_home}"
    elif [[ ! -d "${opt_git_home}" ]]; then
        err=${ERR_GIT_HOME_NOT_DIR}
    fi
    
    if [[ "${err}" == "0" ]]; then
        exec_cmd pushd "${opt_git_home}"
        exec_cmd git clone "${CLONE_REPO_URL}"
        exec_cmd popd
    fi
    
    return "${err}"
}

function make_home_bin_dir() {
    if [[ -e "${HOME_BIN_DIR}" ]]; then
        printf "mkdir %s (directory already exists)\n" "${HOME_BIN_DIR}"
    else
        exec_cmd mkdir "${HOME_BIN_DIR}"
    fi
}

function make_bashrc() {
    local bashrc_file; bashrc_file="${HOME}/.bashrc"
    
    if [[ -e "${bashrc_file}" ]]; then
        printf "%s (file already exists)\n" "${bashrc_file}"
    else
        printf "creating %s\n" "${bashrc_file}"
        
        if [[ "${opt_dry_run}" == 0 ]]; then
            cat > "${HOME}/.bashrc" <<EOF
#!/bin/bash

source ~/.bashrc-common
EOF
        fi
    fi
}

function make_symbolic_links() {
    local jns_src_dir; jns_src_dir="${opt_git_home}/junk-n-stuff/src"
    
    make_os_symbolic_links
    # RC
    make_symbolic_link "${jns_src_dir}/bash/rc/bashrc.sh" "${HOME}/.bashrc-common"
    make_symbolic_link "${jns_src_dir}/bash/rc/inputrc" "${HOME}/.inputrc"
    
    # Bash
    make_symbolic_link "${jns_src_dir}/bash/fnd.sh" "${HOME_BIN_DIR}/fnd"
    make_symbolic_link "${jns_src_dir}/bash/lesspipe.sh" "${HOME_BIN_DIR}/lesspipe"
    make_symbolic_link "${jns_src_dir}/bash/murmur-start.sh" "${HOME_BIN_DIR}/murmur-start"
    make_symbolic_link "${jns_src_dir}/bash/strlen.sh" "${HOME_BIN_DIR}/strlen"
    
    # Python
    make_symbolic_link "${jns_src_dir}/python/alpha.py" "${HOME_BIN_DIR}/alpha"
    make_symbolic_link "${jns_src_dir}/python/kalp/kalp.py" "${HOME_BIN_DIR}/kalp"
    make_symbolic_link "${jns_src_dir}/python/openlatest.py" "${HOME_BIN_DIR}/openlatest"
}

function make_os_symbolic_links() {
    local os; os="$(uname -o)"
    local oslc; oslc="${os,,}"
    
    if [[ "${oslc}" == "gnu/linux" || "${oslc}" == "linux" ]]; then
        printf "creating OS specific symbolic links for %s\n" "${os}"
        make_symbolic_link "${HOME}/Documents" "${HOME}/docs"
        make_symbolic_link "${HOME}/Desktop" "${HOME}/desktop"
    elif [[ "${oslc}" == "cygwin" ]]; then
        printf "creating OS specific symbolic links for %s\n" "${os}"
        make_symbolic_link "/cygdrive/c/Users/${USER}/Documents" "${HOME}/docs"
        make_symbolic_link "/cygdrive/c/Users/${USER}/Desktop" "${HOME}/desktop"
    else
        printf "cannot create OS specific symbolic links unknown OS, %s\n" "${os}"
    fi
}

function make_symbolic_link() {
    local src; src="$1"
    local dest; dest="$2"
    
    if [[ -e "${dest}" ]]; then
        printf "%s (link already exists)\n" "${dest}"
    else
        exec_cmd ln -s "${src}" "${dest}"
    fi
}

main "$@"
