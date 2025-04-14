cmake_minimum_required(VERSION 3.23.0)
project(stdbench)

find_package(benchmark REQUIRED)

add_executable(example benchmarks/copy_if.cpp)
target_link_libraries(example benchmark::benchmark)

