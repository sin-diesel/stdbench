#include <algorithm>
#include <execution>
#include <random>
#include <vector>

int main() {
  long sz = 10000;
  std::random_device RD;
  std::mt19937 MT(RD());

  std::vector<int> v(sz);
  std::iota(v.begin(), v.end(), 0);
  std::shuffle(v.begin(), v.end(), MT);

  for (int i = 0; i < 10000; ++i) {
    auto start = v.begin();
    auto end = start + sz;
    std::transform(std::execution::par, start, end, start, [](int x) { return x * 2; });
  }
  return 0;
}

