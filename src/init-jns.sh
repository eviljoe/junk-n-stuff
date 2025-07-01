#!/bin/bash

set -e # fail on any errors

readonly VERSION="1.2.0"
readonly DEF_CODE_HOME="${HOME}/Documents/code"
readonly DEF_OS="$(uname -o)"
readonly CLONE_REPO_URL="https://github.com/eviljoe/junk-n-stuff.git"

readonly ERR_INVALID_OPT=3
readonly ERR_OPT_REQUIRES_ARG=4
readonly ERR_CODE_HOME_NOT_DIR=5
readonly ERR_NEED_DRY_RUN=6

opt_clone_repo=0
opt_print_help=0
opt_dry_run=0
opt_code_home=""
opt_user_home="${HOME}"
opt_os="${DEF_OS}"
opt_override_symlinks=0

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
            make_home_bin_lib_dir
            make_bashrc
            make_symbolic_links
        fi
    fi
}

function parse_opts {
    local err; err=0

    while getopts ":cdg:ho:su:" opt; do
        case $opt in
            c) opt_clone_repo=1 ;;
            d) opt_dry_run=1 ;;
            g) opt_code_home="${OPTARG}" ;;
            h) opt_print_help=1 ;;
            o) opt_os="${OPTARG}" ;;
            s) opt_override_symlinks=1 ;;
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

    if [[ "${opt_dry_run}" == "0" && "$(str_lower "${opt_os}")" != "$(str_lower "${DEF_OS}")" ]]; then
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
  -c: Clone the junk-n-stuff repo. (default: no)
  -d: Do a dry run.  Do not actually perform any actions. (default: no)
  -g: Git home directory.  (default: ${DEF_CODE_HOME})
  -h: Print this help message and exit
  -o <OS>: Operating system.  Can only be used during dry runs.  (default: ${DEF_OS})
  -s: Overwrite existing symbolic links. (default: no)
  -u <DIR>: User home directory.  (default: ${HOME})

Examples:
  * To init junk-n-stuff: ${base_name}
  * To perform a dry run: ${base_name} -d

Notes:
  * The following key can be used to determine what action was taken for each item:
      + Newly Added
      > Informational Message
      E Already Exists
      R Replaced
  * The Git home directory will be determined using these steps.  If it is found, the subsequent steps will be ignored.
      1. Use the value of the \`-g' option
      2. Use the value of the \`JNS_CODE_HOME' environment variable
      3. Use the default directory: ${DEF_CODE_HOME}
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

function get_code_home {
    local code_home

    if [[ -n "${opt_code_home}" ]]; then
        code_home="${opt_code_home}"
    elif [[ -n "${JNS_CODE_HOME}" ]]; then
        code_home="${JNS_CODE_HOME}"
    else
        code_home="${DEF_CODE_HOME}"
    fi

    printf "%s" "${code_home}"
}

function clone_repo {
    local err; err=0;
    local code_home; code_home="$(get_code_home)"

    if [[ ! -e "${code_home}" ]]; then
        exec_cmd mkdir -p "${code_home}"
    elif [[ ! -d "${code_home}" ]]; then
        err=${ERR_CODE_HOME_NOT_DIR}
    fi

    if [[ "${err}" == "0" ]]; then
        exec_cmd pushd "${opt_code_home}"
        exec_cmd git clone "${CLONE_REPO_URL}"
        exec_cmd popd
    fi

    return "${err}"
}

function make_home_bin_dir {
    local home_bin_dir; home_bin_dir="${opt_user_home}/bin"

    if [[ -e "${home_bin_dir}" ]]; then
        printf "E mkdir %s\n" "${home_bin_dir}"
    else
        printf "+ "
        exec_cmd mkdir "${home_bin_dir}"
    fi
}

function make_home_bin_lib_dir {
    local home_bin_lib_dir; home_bin_lib_dir="${opt_user_home}/bin/lib"

    if [[ -e "${home_bin_lib_dir}" ]]; then
        printf "E mkdir %s\n" "${home_bin_lib_dir}"
    else
        printf "+ "
        exec_cmd mkdir "${home_bin_lib_dir}"
    fi
}

function make_bashrc {
    local bashrc_file; bashrc_file="${opt_user_home}/.bashrc"

    if [[ -e "${bashrc_file}" ]]; then
        printf "E %s\n" "${bashrc_file}"
    else
        printf "+ %s\n" "${bashrc_file}"

        if [[ "${opt_dry_run}" == 0 ]]; then
            cat > "${opt_user_home}/.bashrc" <<EOF
#!/bin/bash

source ~/.bashrc-common
EOF
        fi
    fi
}

function make_symbolic_links {
    local jns_src_dir; jns_src_dir="$(get_code_home)/junk-n-stuff/src"
    local home_bin_dir; home_bin_dir="${opt_user_home}/bin"

    make_os_symbolic_links

    # RC
    printf "> creating RC symbolic links\n"
    make_symbolic_link "${jns_src_dir}/rc/bashrc.sh"          "${opt_user_home}/.bashrc-common"
    make_symbolic_link "${jns_src_dir}/rc/emacs"              "${opt_user_home}/.emacs"
    make_symbolic_link "${jns_src_dir}/rc/gitconfig.toml"     "${opt_user_home}/.gitconfig"
    make_symbolic_link "${jns_src_dir}/rc/inputrc"            "${opt_user_home}/.inputrc"
    make_symbolic_link "${jns_src_dir}/rc/tmux.conf"          "${opt_user_home}/.tmux.conf"
    make_symbolic_link "${jns_src_dir}/rc/tmux.conf.8color"   "${opt_user_home}/.tmux.conf.8color"
    make_symbolic_link "${jns_src_dir}/rc/tmux.conf.256color" "${opt_user_home}/.tmux.conf.256color"
    make_symbolic_link "${jns_src_dir}/rc/vimrc"              "${opt_user_home}/.vimrc"

    # Scripts
    printf "> creating executable symbolic links - user commands\n"
    make_symbolic_link "${jns_src_dir}/catvids.py"            "${home_bin_dir}/catvids"
    make_symbolic_link "${jns_src_dir}/cheat.py"              "${home_bin_dir}/cheat"
    make_symbolic_link "${jns_src_dir}/compare-hashdeep.bash" "${home_bin_dir}/compare-hashdeep"
    make_symbolic_link "${jns_src_dir}/fnd.sh"                "${home_bin_dir}/fnd"
    make_symbolic_link "${jns_src_dir}/init-jns.sh"           "${home_bin_dir}/init-jns"
    make_symbolic_link "${jns_src_dir}/lesspipe.sh"           "${home_bin_dir}/lesspipe"
    make_symbolic_link "${jns_src_dir}/openlatest.py"         "${home_bin_dir}/openlatest"
    make_symbolic_link "${jns_src_dir}/prefix-with-dir.bash"  "${home_bin_dir}/prefix-with-dir"
    make_symbolic_link "${jns_src_dir}/psgrep.sh"             "${home_bin_dir}/psgrep"
    make_symbolic_link "${jns_src_dir}/strindexof.py"         "${home_bin_dir}/strindexof"
    make_symbolic_link "${jns_src_dir}/strlen.sh"             "${home_bin_dir}/strlen"
    make_symbolic_link "${jns_src_dir}/unite.py"              "${home_bin_dir}/unite"
    make_symbolic_link "${jns_src_dir}/ununite.py"            "${home_bin_dir}/ununite"

    # Git Scripts
    make_symbolic_link_git "${jns_src_dir}/gitbp.py"          "${home_bin_dir}" "gitbp"          "git-bp"
    make_symbolic_link_git "${jns_src_dir}/gitlog1.bash"      "${home_bin_dir}" "gitlog1"        "git-log1"
    make_symbolic_link_git "${jns_src_dir}/gitquicksave.py"   "${home_bin_dir}" "gitquicksave"   "git-quicksave"
    make_symbolic_link_git "${jns_src_dir}/gitrebasechain.py" "${home_bin_dir}" "gitrebasechain" "git-rebase-chain"
    make_symbolic_link_git "${jns_src_dir}/gitroh.py"         "${home_bin_dir}" "gitroh"         "git-roh"
    make_symbolic_link_git "${jns_src_dir}/gitrom.py"         "${home_bin_dir}" "gitrom"         "git-rom"

    # Lib Scripts - tmux
    printf "> creating executable symbolic links - lib/tmux\n"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_get_tmux_major_version.sh"      "${home_bin_dir}/lib/_get_tmux_major_version"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_get_tmux_minor_version.sh"      "${home_bin_dir}/lib/_get_tmux_minor_version"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_get_tmux_version.sh"            "${home_bin_dir}/lib/_get_tmux_version"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_is_tmux_in_cygwin.sh"           "${home_bin_dir}/lib/_is_tmux_in_cygwin"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_is_tmux_in_linux_with_xclip.sh" "${home_bin_dir}/lib/_is_tmux_in_linux_with_xclip"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_is_tmux_v1.sh"                  "${home_bin_dir}/lib/_is_tmux_v1"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_is_tmux_v2_0__2_3m.sh"          "${home_bin_dir}/lib/_is_tmux_v2_0__2_3m"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_is_tmux_v2_4p.sh"               "${home_bin_dir}/lib/_is_tmux_v2_4p"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_is_tmux_v2.sh"                  "${home_bin_dir}/lib/_is_tmux_v2"
    make_symbolic_link "${jns_src_dir}/tmuxlib/_is_tmux_v2p.sh"                 "${home_bin_dir}/lib/_is_tmux_v2p"
}

function make_os_symbolic_links {
    local oslc; oslc="$(str_lower "${opt_os}")"

    if [[ "${oslc}" == "gnu/linux" || "${oslc}" == "linux" ]]; then
        printf "> creating OS specific symbolic links for %s\n" "${opt_os}"
        make_symbolic_link "${opt_user_home}/Documents" "${opt_user_home}/docs"
        make_symbolic_link "${opt_user_home}/Desktop"   "${opt_user_home}/desktop"
    elif [[ "${oslc}" == "cygwin" ]]; then
        local winhome

        printf "> creating OS specific symbolic links for %s\n" "${opt_os}"

        # The `cygpath' command only exists in Cygwin, and the `USERPROFILE' env. var. only exists in Windows
        # environments.  This check is to make sure the script does not error out when manually specifying the OS to be
        # Cygwin.
        if which cygpath &>/dev/null && [[ -v HOME ]]; then
            winhome="$(cygpath "${USERPROFILE}")"
        else
            winhome="/cygdrive/c/Users/${USER}"
        fi

        make_symbolic_link "${winhome}"           "${opt_user_home}/winhome"
        make_symbolic_link "${winhome}/Documents" "${opt_user_home}/Documents"
        make_symbolic_link "${winhome}/Documents" "${opt_user_home}/docs"
        make_symbolic_link "${winhome}/Desktop"   "${opt_user_home}/desktop"
    else
        printf "> cannot create OS specific symbolic links unknown OS, %s\n" "${opt_os}"
    fi
}

function make_symbolic_link {
    local src; src="$1"
    local dest; dest="$2"

    # If a symlink / file already exists, check to see if it should be replaced
    if [[ -e "${dest}" || -L "${dest}" ]]; then
        # If overriding existing symlinks, make sure the symlink to replace is actually a symlink.  If it is not a
        # symlink, it should not be replaced.
        if [[ "${opt_override_symlinks}" == "1" && -L "${dest}" ]]; then
            rm "${dest}"
            printf "R "
            exec_cmd ln -s "${src}" "${dest}"
        else
            printf "E ln -s \"%s\" \"%s\"\n" "${src}" "${dest}"
        fi
    else
        printf "+ "
        exec_cmd ln -s "${src}" "${dest}"
    fi
}

function make_symbolic_link_git {
    local src; src="$1"
    local dest_dir; dest_dir="$2"
    local direct_name; direct_name="$3"
    local subcommand_name; subcommand_name="$4"

    make_symbolic_link "${src}" "${dest_dir}/${direct_name}"
    make_symbolic_link "${src}" "${dest_dir}/${subcommand_name}"
}

function str_lower {
    printf "%s" "$1" | tr "[:upper:]" "[:lower:]"
}

main "$@"
