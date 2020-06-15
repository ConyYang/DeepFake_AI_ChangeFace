#!/usr/bin/env bash

source venv/bin/activate

echo 'Fetching...'
python fetch.py -k "${1}"

echo 'Downloading...'
python download.py
