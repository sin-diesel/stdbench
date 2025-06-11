#!/usr/bin/bash

SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

COMPILERS="g++"

for COMPILER in $COMPILERS; do
  ctest --test-dir build/$COMPILER -j10
done

