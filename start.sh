#!/bin/sh

# This file runs all setup needed to use repo
# - create python env and activate
# - setup cohere key as env var

# 1
#python3 -m venv env
#source env/bin/activate
#python install -r requirements.txt

# 2
export COHERE_API_KEY=$(cat *key)

# 3
python main.py