#!/usr/bin/bash

COMPILERS="g++ clang++-18"

for COMPILER in $COMPILERS; do
  cmake -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake -DCMAKE_CXX_COMPILER=$COMPILER -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release -B build/$COMPILER
done

for COMPILER in $COMPILERS; do
  cmake --build build/$COMPILER
done

