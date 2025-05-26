import os
import pytest
from pathlib import Path

from stdbench.benchmark import Benchmark, BenchGenerator
from stdbench.plotter import Plotter

_repo_root = Path(__file__).parent.parent

def test_benchmarks_generation():
    config_path = _repo_root / "tests" / "config.yaml"
    bench_generator = BenchGenerator(config_path, templates_path=_repo_root / "templates")
    benchmarks = bench_generator.generate()

def test_benchmarks_plotting():
    config_path = _repo_root / "tests" / "config.yaml"
    bench_generator = BenchGenerator(config_path, templates_path=_repo_root / "templates")
    benchmarks = bench_generator.generate()

    output_folder = _repo_root / "build"
    plotter = Plotter(output_folder)
    plotter.plot(name="all_of", T="int", src_container="std::vector", policy="par_unseq", compiler_opts="-O2", func="[](int i) { return i % 2 == 0; }", compiler="clang++-19")

