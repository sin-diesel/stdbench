#!/usr/bin/bash

pdm run black $PROJECT_SRC_REL $PROJECT_SETUP
pdm run flake8 --ignore F401 --max-line-length 120 $PROJECT_SRC_REL $PROJECT_SETUP

