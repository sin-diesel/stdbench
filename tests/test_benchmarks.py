from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from stdbench.benchmark import Benchmark

def test_benchmark():
    env = Environment(loader=FileSystemLoader("templates"))
    benchmark = Benchmark(env=env, template="input_range_output_iterator.jinja", output_dir=Path("benchmarks"))
    benchmark.generate("copy", src_container="std::vector", T="int", size=1000, dst_container="std::vector")

