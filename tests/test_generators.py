import os
import pytest
import subprocess
from pathlib import Path

from stdbench.bench_generator import Benchmark, BenchGenerator
from stdbench.test_generator import TestGenerator
from stdbench.config import Config
from stdbench.results_analyzer import ResultsAnalyzer

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

def test_bench_generator():
    config = Config(_repo_root / "tests" / "config.yaml")
    bench_generator = BenchGenerator(config=config, output_dir = _repo_root / "build" / "benchmarks",  templates_path = _repo_root / "templates")
    benchmarks = bench_generator.generate()
    assert len(benchmarks) > 0
    assert len(os.listdir(_repo_root / "build" / "benchmarks")) > 0

    assert (_repo_root / "build" / "benchmarks" / "hints.cmake").exists()


def test_test_generator():
    config = Config(_repo_root / "tests" / "config.yaml")
    bench_generator = BenchGenerator(config=config, output_dir = _repo_root / "build" / "benchmarks",  templates_path = _repo_root / "templates")
    benchmarks = bench_generator.generate()

    test_generator = TestGenerator(config=config, build_path=_repo_root / "build", benchmarks=benchmarks)
    cmake_tests = test_generator.generate()
    assert len(cmake_tests) > 0


def test_tmp_results():
    config = Config(_repo_root / "tests" / "config.yaml")
    bench_generator = BenchGenerator(config=config, output_dir = _repo_root / "build" / "benchmarks",  templates_path = _repo_root / "templates")
    benchmarks = bench_generator.generate()

    test_generator = TestGenerator(config=config, build_path=_repo_root / "build", benchmarks=benchmarks)
    cmake_tests = test_generator.generate()
    assert len(cmake_tests) > 0


def test_e2e():
    config = Config(_repo_root / "tests" / "config.yaml")
    bench_generator = BenchGenerator(config=config, output_dir = _repo_root / "build" / "benchmarks",  templates_path = _repo_root / "templates")
    benchmarks = bench_generator.generate()

    test_generator = TestGenerator(config=config, build_path=_repo_root / "build", benchmarks=benchmarks)
    cmake_tests = test_generator.generate()

    subprocess.run(["bash", "build.sh"], cwd=_repo_root)
    subprocess.run(["bash", "test.sh"], cwd=_repo_root)

    #results_analyzer = ResultsAnalyzer(cmake_tests)


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
