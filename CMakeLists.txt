cmake_minimum_required(VERSION 3.23.0)
project(stdbench)

set(benchmarks_path "build/benchmarks")
include(${benchmarks_path}/hints.cmake)

find_package(benchmark REQUIRED)

file(GLOB benchmarks "${benchmarks_path}/*.cpp")
enable_testing()
get_filename_component(base_compiler_name ${CMAKE_CXX_COMPILER} NAME_WE)


function(add_stdbench_test bare_name benchmark size compiler_opts_value)
   set(test_name "${bare_name}_${compiler_opts_value}_${size}")
   set(executable_name "${bare_name}_${compiler_opts_value}")

   add_test(NAME
      ${test_name}
      COMMAND
      sh -c "echo ${size} | ${CMAKE_BINARY_DIR}/${executable_name} \
      --benchmark_out_format=json \
      --benchmark_out=${test_name}.json \
      --benchmark_context=compiler=${base_compiler_name} \
      --benchmark_context=compiler_opts=${compiler_opts_value}"
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
   )
   set_tests_properties(${test_name} PROPERTIES TIMEOUT 10)

endfunction()

foreach(benchmark ${benchmarks})
   foreach (compiler_opts_value ${compiler_options})
      message("benchmark = " ${benchmark})
      get_filename_component(bare_name ${benchmark} NAME_WE)
      message(${bare_name})

      set(executable_name "${bare_name}_${compiler_opts_value}")
      add_executable(${executable_name} ${benchmark})

      target_compile_options(${executable_name} PRIVATE ${compiler_opts_value})
      target_link_libraries(${executable_name} benchmark::benchmark)
      foreach (size_value ${size})
         add_stdbench_test(${bare_name} ${benchmark} ${size_value} ${compiler_opts_value})
      endforeach()
    endforeach()
endforeach()

