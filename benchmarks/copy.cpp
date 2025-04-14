
#include <algorithm>
#include <execution>
#include <numeric>

#include <benchmark/benchmark.h>

static void BM_copy(benchmark::State& state) {
 
std::vector<int> test_from_container(10000);
std::iota(test_from_container.begin(), test_from_container.end(), 0);
std::vector<int> test_dest_container;
        

 for (auto _: state) {
   std::copy(std::execution::par, test_from_container.begin(), test_from_container.end(),   std::back_inserter(test_dest_container), [](int x) { return x % 3 == 0; } );
   }
}

BENCHMARK(BM_copy);;

BENCHMARK_MAIN();;