#!/bin/sh

# This file runs all setup needed to use repo
# - create python env and activate
# - setup cohere key as env var

# 1
python3.11 -m venv env
env/bin/pip install -r requirements.txt

# 2
export COHERE_API_KEY=$(cat *key)

# 3
sentence="$1"
env/bin/python main.py "$sentence"
