cmake_minimum_required(VERSION 3.23.0)
project(stdbench)

find_package(benchmark REQUIRED)

file(GLOB benchmarks "benchmarks/*.cpp")
enable_testing()
foreach(benchmark ${benchmarks})
    get_filename_component(test_name ${benchmark} NAME_WE)
    add_executable(${test_name} ${benchmark})
    target_link_libraries(${test_name} benchmark::benchmark)
    add_test(NAME ${test_name} COMMAND ${test_name})
endforeach()

