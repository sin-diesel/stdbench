cmake_minimum_required(VERSION 3.23.0)
project(stdbench)

add_custom_target(benchmarks)

file(GLOB BENCHMARKS
  "${BENCHMARKS_FOLDER}/*.cpp"
)

find_package(cppbenchmark REQUIRED)

foreach (FILE ${BENCHMARKS})
  get_filename_component(TARGET_NAME ${FILE} NAME_WE)
  add_executable(${TARGET_NAME} ${FILE})
  target_link_libraries(${TARGET_NAME} cppbenchmark::cppbenchmark)
endforeach()

