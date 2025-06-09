#!/usr/bin/bash

SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

COMPILERS="g++ clang++-19"

for COMPILER in $COMPILERS; do
  ctest --test-dir build/$COMPILER -j8
done

