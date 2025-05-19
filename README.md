# stdbench
Python library designed for generating C++ standard library algorithms benchmarks.

# Installing dependencies

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

# Running tests
```bash
pdm sync
source .venv/bin/activate
conan install . -s compiler.cppstd=17 -s compiler.version=11 
pdm run pytest -o log_level=DEBUG -o log_cli=True tests/test_benchmarks.py
bash ./build.sh
```

