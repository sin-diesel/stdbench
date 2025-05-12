cmake_minimum_required(VERSION 3.23.0)
project(stdbench)

include("benchmarks/cmake_env_vars.cmake")

find_package(benchmark REQUIRED)

file(GLOB benchmarks "benchmarks/*.cpp")
enable_testing()
foreach (compiler ${COMPILER})
    foreach (compiler_opts ${COMPILER_OPTS})
        foreach(benchmark ${benchmarks})
            #set(CMAKE_CXX_COMPILER ${compiler})
            #add_compile_options(${compiler_opts})
            get_filename_component(test_name ${benchmark} NAME_WE)
            set(test_name "${test_name}_${compiler}_${compiler_opts}") 
            add_executable(${test_name} ${benchmark})
            target_link_libraries(${test_name} benchmark::benchmark)
            add_test(NAME ${test_name} COMMAND ${test_name} --benchmark_out_format=json --benchmark_out=${test_name}.json)
        endforeach()
    endforeach()
endforeach()

