
pdm run black $PROJECT_SRC_REL
pdm run flake8 --max-line-length 120 --ignore F401,W503 $PROJECT_SRC_REL

