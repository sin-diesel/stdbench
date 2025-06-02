import os
import pytest
from pathlib import Path

from stdbench.benchmark import Benchmark, BenchGenerator
from stdbench.config import Config
from stdbench.results_analyzer import Measurement

_repo_root = Path(__file__).parent.parent

def test_config():
    config = Config(_repo_root / "tests" / "config.yaml")
    assert config
    benchmark_config = config.benchmark_config()
    assert "name" in benchmark_config.keys()

    benchmark_config_transposed = config.benchmark_config(transposed=True)
    assert isinstance(benchmark_config_transposed[0], list)
    assert isinstance(benchmark_config_transposed[0][0], dict)

    environment_config = config.environment_config()
    assert "compiler" in environment_config.keys()

def test_generator():
    bench_generator = BenchGenerator(config_path=_repo_root / "tests" / "config.yaml", output_dir = _repo_root / "build" / "benchmarks",  templates_path = _repo_root / "templates")
    benchmarks = bench_generator.generate()
    assert len(benchmarks) > 0
    assert len(os.listdir(_repo_root / "build" / "benchmarks")) > 0

    assert (_repo_root / "build" / "benchmarks" / "hints.cmake").exists()

def test_measurement():
    config = Config(_repo_root / "tests" / "config.yaml")
    measurement = Measurement(config)

    benchmark_configs = config.benchmark_params()
    for config in benchmark_configs:
        assert hasattr(measurement, config)

#def test_benchmarks_generation():
#    config_path = _repo_root / "tests" / "config.yaml"
#    bench_generator = BenchGenerator(config_path, templates_path=_repo_root / "templates")
#    benchmarks = bench_generator.generate()
#
#def test_benchmarks_plotting():
#    config_path = _repo_root / "tests" / "config.yaml"
#    bench_generator = BenchGenerator(config_path, templates_path=_repo_root / "templates")
#    benchmarks = bench_generator.generate()
#
#    output_folder = _repo_root / "build"
#    plotter = Plotter(output_folder)
#    plotter.plot(name="all_of", T="int", src_container="std::vector", policy="par_unseq", compiler_opts="-O2", func="[](int i) { return i % 2 == 0; }", compiler="clang++-19")
#
#def test_benchmarks_plot_all():
#    config_path = _repo_root / "tests" / "config.yaml"
#    bench_generator = BenchGenerator(config_path, templates_path=_repo_root / "templates")
#    benchmarks = bench_generator.generate()
#
#    output_folder = _repo_root / "build"
#    plotter = Plotter(output_folder)
#    plotter.plot_all(bench_generator.benchmark_configs())
#
