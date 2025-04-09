#!/bin/bash

set -euo pipefail

directory="$1"

if ! [ -d "${directory}" ]; then
    printf '%s is not a directory\n' "${directory}" 1>&2
    exit 1
fi

directory_realpath="$(realpath "${directory}")"
directory_name="$(basename "${directory_realpath}")"

cd "${directory}" || exit 1

for f in "${directory_realpath}/"*; do
    new_file_name="${directory_name}-$(basename "${f}")"
    printf '%s\n' "${new_file_name}"
    mv "${f}" "${new_file_name}"
done
