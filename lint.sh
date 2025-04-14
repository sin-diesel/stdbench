
pdm run black $PROJECT_SRC_REL
pdm run flake8 --ignore F401 --max-line-length 130 $PROJECT_SRC_REL

