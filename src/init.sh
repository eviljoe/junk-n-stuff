#!/bin/bash

set -e # fail on any errors

readonly DEF_GIT_HOME="${HOME}/Documents/git"
readonly DEF_OS="$(uname -o)"
readonly CLONE_REPO_URL="https://github.com/eviljoe/junk-n-stuff.git"

readonly ERR_INVALID_OPT=3
readonly ERR_OPT_REQUIRES_ARG=4
readonly ERR_GIT_HOME_NOT_DIR=5
readonly ERR_NEED_DRY_RUN=6

opt_clone_repo=0
opt_print_help=0
opt_dry_run=0
opt_git_home="${DEF_GIT_HOME}"
opt_user_home="${HOME}"
opt_os="${DEF_OS}"

function main {
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

function parse_opts {
    local err; err=0
    
    while getopts ":cdg:ho:u:" opt; do
        case $opt in
            c) opt_clone_repo=1 ;;
            d) opt_dry_run=1 ;;
            g) opt_git_home="${OPTARG}" ;;
            h) opt_print_help=1 ;;
            o) opt_os="${OPTARG}" ;;
            u) opt_user_home="${OPTARG}" ;;
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
    
    if [[ "${opt_dry_run}" == "0" && "${opt_os,,}" != "${DEF_OS,,}" ]]; then
        err=${ERR_NEED_DRY_RUN}
        printf "When specifying an OS, must do a dry run.\n" 1>&2
    fi
    
    if [[ "${err}" != "0" ]]; then
        printf "For correct usage, execute: %s -h\n" "$(basename $0)" 1>&2
    fi
    
    return ${err}
}

function print_help {
    local base_name; base_name="$(basename "$0")"
    
    fold -w "$(tput cols)" <<EOF
${base_name}: A script to init junk-n-stuff
Version: ${VERSION}

Usage: ${base_name} [options]
Options:
  -c: Clone repo junk-n-stuff repo
  -d: Do a dry run.  Do not actually perform any actions.
  -g: Git home directory.  (default: ${DEF_GIT_HOME})
  -h: Print this help message and exit
  -o: Operating system.  Can only be used during dry runs.  (default: ${DEF_OS})
  -u: User home directory.  (default: ${HOME})

Examples:
  To init junk-n-stuff: ${base_name}
  To perform a dry run: ${base_name} -d
EOF
}

function exec_cmd {
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

function clone_repo {
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

function make_home_bin_dir {
    local home_bin_dir; home_bin_dir="${opt_user_home}/bin"
    
    if [[ -e "${home_bin_dir}" ]]; then
        printf "mkdir %s (directory already exists)\n" "${home_bin_dir}"
    else
        exec_cmd mkdir "${home_bin_dir}"
    fi
}

function make_bashrc {
    local bashrc_file; bashrc_file="${opt_user_home}/.bashrc"
    
    if [[ -e "${bashrc_file}" ]]; then
        printf "%s (file already exists)\n" "${bashrc_file}"
    else
        printf "creating %s\n" "${bashrc_file}"
        
        if [[ "${opt_dry_run}" == 0 ]]; then
            cat > "${opt_user_home}/.bashrc" <<EOF
#!/bin/bash

source ~/.bashrc-common
EOF
        fi
    fi
}

function make_symbolic_links {
    local jns_src_dir; jns_src_dir="${opt_git_home}/junk-n-stuff/src"
    local home_bin_dir; home_bin_dir="${opt_user_home}/bin"
    
    make_os_symbolic_links
    
    # RC
    make_symbolic_link "${jns_src_dir}/rc/bashrc.sh" "${opt_user_home}/.bashrc-common"
    make_symbolic_link "${jns_src_dir}/rc/inputrc" "${opt_user_home}/.inputrc"
    
    # Bash
    make_symbolic_link "${jns_src_dir}/fnd.sh" "${home_bin_dir}/fnd"
    make_symbolic_link "${jns_src_dir}/lesspipe.sh" "${home_bin_dir}/lesspipe"
    make_symbolic_link "${jns_src_dir}/murmur-start.sh" "${home_bin_dir}/murmur-start"
    make_symbolic_link "${jns_src_dir}/strlen.sh" "${home_bin_dir}/strlen"
    
    # Python
    make_symbolic_link "${jns_src_dir}/alpha.py" "${home_bin_dir}/alpha"
    make_symbolic_link "${jns_src_dir}/kalp/kalp.py" "${home_bin_dir}/kalp"
    make_symbolic_link "${jns_src_dir}/openlatest.py" "${home_bin_dir}/openlatest"
}

function make_os_symbolic_links {
    local oslc; oslc="${opt_os,,}"
    
    if [[ "${oslc}" == "gnu/linux" || "${oslc}" == "linux" ]]; then
        printf "creating OS specific symbolic links for %s\n" "${opt_os}"
        make_symbolic_link "${opt_user_home}/Documents" "${opt_user_home}/docs"
        make_symbolic_link "${opt_user_home}/Desktop" "${opt_user_home}/desktop"
    elif [[ "${oslc}" == "cygwin" ]]; then
        printf "creating OS specific symbolic links for %s\n" "${opt_os}"
        make_symbolic_link "/cygdrive/c/Users/${USER}/Documents" "${opt_user_home}/Documents"
        make_symbolic_link "/cygdrive/c/Users/${USER}/Documents" "${opt_user_home}/docs"
        make_symbolic_link "/cygdrive/c/Users/${USER}/Desktop" "${opt_user_home}/desktop"
    else
        printf "cannot create OS specific symbolic links unknown OS, %s\n" "${opt_os}"
    fi
}

function make_symbolic_link {
    local src; src="$1"
    local dest; dest="$2"
    
    if [[ -e "${dest}" ]]; then
        printf "(link already exists) ln -s \"%s\" \"%s\"\n" "${src}" "${dest}"
    else
        exec_cmd ln -s "${src}" "${dest}"
    fi
}

main "$@"
