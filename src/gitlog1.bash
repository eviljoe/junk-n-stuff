#!/bin/bash

git log --format=oneline --abbrev-commit --no-decorate "$@"
