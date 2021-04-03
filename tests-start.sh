#!/usr/bin/env bash

set -e

export TESTING=True

python app/tests_pre_start.py

bash ./scripts/test.sh "$@"

echo "I am done testing!"
unset TESTING