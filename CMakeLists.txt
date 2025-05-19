cmake_minimum_required(VERSION 3.23.0)
project(stdbench)

include("build/benchmarks/compiler_opts.cmake")

find_package(benchmark REQUIRED)

file(GLOB benchmarks "build/benchmarks/*.cpp")
enable_testing()
foreach (compiler_opts ${COMPILER_OPTS})
    foreach(benchmark ${benchmarks})
       get_filename_component(test_name ${benchmark} NAME_WE)
       set(test_name "${test_name}_${compiler_opts}") 
       add_executable(${test_name} ${benchmark})
       target_compile_options(${test_name} PRIVATE ${compiler_opts})
       target_link_libraries(${test_name} benchmark::benchmark)
       add_test(NAME ${test_name} COMMAND ${test_name} --benchmark_out_format=json --benchmark_out=${test_name}.json)
    endforeach()
endforeach()

