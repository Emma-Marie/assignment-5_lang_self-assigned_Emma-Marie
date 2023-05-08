#!/usr/bin/env bash

#create virtual environment
python3 -m venv sermons_env
source ./sermons_env/bin/activate

# requirements
pip install --upgrade pip
pip install --upgrade nbformat
python3 -m pip install -r requirements.txt

#deactivate the venv
deactivate