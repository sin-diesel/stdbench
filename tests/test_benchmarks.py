from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from stdbench.benchmark import Benchmark

def test_benchmarks():
    env = Environment(loader=FileSystemLoader("templates"))
    copy = Benchmark(name="copy", env=env, template="input_range_output_iterator.jinja", output_dir=Path("benchmarks"))
    copy.generate(src_container="std::vector", T="int", size=1000, dst_container="std::vector")

    for_each = Benchmark(name="for_each", env=env, template="input_range.jinja", output_dir=Path("benchmarks"))
    for_each.generate(src_container="std::vector", T="int", size=1000, func="[](int &n) { n++; }")

    for_each_n = Benchmark(name="for_each_n", env=env, template="input_range_value.jinja", output_dir=Path("benchmarks"))
    for_each_n.generate(src_container="std::vector", T="int", size=1000, last=3, func="[](auto& n) { n *= 2; }")

    all_of = Benchmark(name="all_of", env=env, template="input_range.jinja", output_dir=Path("benchmarks"))
    all_of.generate(src_container="std::vector", T="int", size=1000, func="[](int i) { return i % 2 == 0; }")

    any_of = Benchmark(name="any_of", env=env, template="input_range.jinja", output_dir=Path("benchmarks"))
    any_of.generate(src_container="std::vector", T="int", size=1000, func="[](int i) { return i % 2 == 0; }")

    none_of = Benchmark(name="none_of", env=env, template="input_range.jinja", output_dir=Path("benchmarks"))
    none_of.generate(src_container="std::vector", T="int", size=1000, func="[](int i) { return i % 2 == 0; }")

    find_if = Benchmark(name="find_if", env=env, template="input_range.jinja", output_dir=Path("benchmarks"))
    find_if.generate(src_container="std::vector", T="int", size=1000, func="[](int i) { return i % 2 == 0; }")

