#!/usr/bin/env bash

set -e

export TESTING=True
export PROJECT_NAME=oscarine-api
export BACKEND_CORS_ORIGINS=http://localhost:8000
export SECRET_KEY=my-secret-key-for-testing

python app/tests_pre_start.py

alembic upgrade head

bash ./scripts/test.sh "$@"

echo "I am done testing!"
unset TESTING
unset PROJECT_NAME
unset BACKEND_CORS_ORIGINS
unset SECRET_KEY
