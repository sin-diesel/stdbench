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
python3 -m stdbench # Generate tests
bash ./build.sh # Change your compilers here
bash ./test.sh # Change your compilers here
```

