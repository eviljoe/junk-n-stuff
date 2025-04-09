#!/bin/bash

set -euo pipefail

# Compare the output hashes created by running `hashdeep'.
# Example:
#   compare-hashdeep hashdeep-hdd2-media.txt hashdeep-hdd3-media.txt /mnt/hdd2/ /mnt/hdd3/

hash_file1="$1"
hash_file2="$2"
parent_path1="$3"
parent_path2="$4"
tmp_dir="$(mktemp -d -t compare-hashdeep-XXXXX)"

sort "${hash_file1}" --field-separator=',' --key=4 > "${tmp_dir}/normalized-hashes1.txt"
sort "${hash_file2}" --field-separator=',' --key=4 | sed -e "s#${parent_path2}#${parent_path1}#" > "${tmp_dir}/normalized-hashes2.txt"

diff "${tmp_dir}/normalized-hashes1.txt" "${tmp_dir}/normalized-hashes2.txt"
