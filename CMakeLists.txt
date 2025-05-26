cmake_minimum_required(VERSION 3.23.0)
project(stdbench)

include("build/benchmarks/compiler_opts.cmake")

find_package(benchmark REQUIRED)

file(GLOB BENCHMARKS "build/benchmarks/*.cpp")
enable_testing()
foreach (COMPILER_OPT ${COMPILER_OPTS})
   foreach(BENCHMARK ${BENCHMARKS})
       get_filename_component(TEST_NAME ${BENCHMARK} NAME_WE)
       set(TEST_NAME "${TEST_NAME}_${COMPILER_OPT}") 
       add_executable(${TEST_NAME} ${BENCHMARK})
       target_compile_options(${TEST_NAME} PRIVATE ${COMPILER_OPTS})
       target_link_libraries(${TEST_NAME} benchmark::benchmark)
       add_test(NAME
          ${TEST_NAME}
          COMMAND
          ${TEST_NAME}
          --benchmark_out_format=json
          --benchmark_out=${TEST_NAME}.json
          --benchmark_context=compiler=${CXX}
          --benchmark_context=compiler_opts=${COMPILER_OPTS}
       )
    endforeach()
endforeach()

