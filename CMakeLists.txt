cmake_minimum_required(VERSION 3.10)
project(stdbench)

add_custom_target(benchmarks)

file(GLOB BENCHMARKS
  "${BENCHMARKS_FOLDER}/*.cpp"
)


foreach (FILE ${BENCHMARKS})
  get_filename_component(TARGET_NAME ${FILE} NAME_WE)
  add_executable(${TARGET_NAME} ${FILE})
endforeach()

