#include <benchmark/benchmark.h>
#include <numeric>

static void BM_Copy(benchmark::State& state) {
  std::vector<int> from_vector(100000000);
  std::iota(from_vector.begin(), from_vector.end(), 0);
  std::vector<int> to_vector;

  for (auto _: state) {
    std::copy(from_vector.begin(), from_vector.end(), std::back_inserter(to_vector));
  }
}


BENCHMARK(BM_Copy);

BENCHMARK_MAIN();

