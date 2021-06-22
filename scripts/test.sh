#!/usr/bin/env bash

set -e
set -x

pytest --timeout=60 --timeout_method=thread