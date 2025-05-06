# stdbench
Python library designed for generating C++ standard library algorithms benchmarks.

# Installing dependencies

curl -sSL https://pdm-project.org/install-pdm.py | python3 -

# Running tests
pdm sync
source .venv/bin/activate
conan install . -s compiler.cppstd=17 -s compiler.version=11 
cmake --preset conan-release
cmake --build build/Release
cmake --test-dir build/Release

