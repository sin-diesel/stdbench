#!/usr/bin/bash

SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

COMPILERS="g++ clang++-19"

for COMPILER in $COMPILERS; do
  cmake -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=$SCRIPT_DIR/build/conan_toolchain.cmake -DCMAKE_CXX_COMPILER=$COMPILER -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release -B $SCRIPT_DIR/build/$COMPILER
done

for COMPILER in $COMPILERS; do
  cmake --build build/$COMPILER
done


