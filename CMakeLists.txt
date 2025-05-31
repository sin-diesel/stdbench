cmake_minimum_required(VERSION 3.23.0)
project(stdbench)

find_package(benchmark REQUIRED)

file(GLOB BENCHMARKS "build/benchmarks/*.cpp")
enable_testing()
get_filename_component(BASE_COMPILER_NAME ${CMAKE_CXX_COMPILER} NAME_WE)


function(add_stdbench_test benchmark size compiler_opts)
   get_filename_component(bare_name ${benchmark} NAME_WE)

   set(executable_name "${bare_name}_${compiler_opts}")
   add_executable(${executable_name})

   target_compile_options(${executable_name} PRIVATE ${compiler_opts})
   target_link_libraries(${executable_name} benchmark::benchmark)

   set(benchmark_name "${bare_name}_${size}_${compiler_opts}")

   add_test(NAME
      ${benchmark_name}
      COMMAND
      ${benchmark_name}
      ${size}
      --benchmark_out_format=json
      --benchmark_out=${benchmark_name}.json
      --benchmark_context=compiler=${BASE_COMPILER_NAME}
      --benchmark_context=compiler_opts=${compiler_opts}

)

endfunction()

foreach (SIZE ${INPUT_SIZE})
   foreach (COMPILER_OPT ${COMPILER_OPTS})
   foreach(BENCHMARK ${BENCHMARKS})
       get_filename_component(TEST_NAME ${BENCHMARK} NAME_WE)
       set(TEST_NAME "${TEST_NAME}_${COMPILER_OPT}") 
       add_executable(${TEST_NAME} ${BENCHMARK})
       target_link_libraries(${TEST_NAME} benchmark::benchmark)
       add_test(NAME
          ${TEST_NAME}
          COMMAND
          ${TEST_NAME}
          --benchmark_out_format=json
          --benchmark_out=${TEST_NAME}.json
          --benchmark_context=compiler=${BASE_COMPILER_NAME}
          --benchmark_context=compiler_opts=${COMPILER_OPTS}
       )
    endforeach()
endforeach()

