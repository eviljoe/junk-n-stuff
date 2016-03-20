#!/bin/bash

py_src_dir="$(dirname "$0")/../src"

python3 -m unittest discover -p "*_test.py" -s "${py_src_dir}"