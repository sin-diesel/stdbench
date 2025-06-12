from pathlib import Path

from stdbench.config import Config
from stdbench.bench_generator import BenchGenerator
from stdbench.test_generator import TestGenerator
from stdbench.results_analyzer import ResultsAnalyzer

_repo_root = Path(__file__).parent.parent

def test_config():
    config = Config(_repo_root / "tests" / "config.yaml")
    assert config
    assert len(config.benchmark_configs) >  0
    assert config.benchmark_configs[0].name != ""

    assert config.benchmark_configs[0].environment["compiler_options"] == ["-O2"] or \
    config.benchmark_configs[0].environment["compiler_options"] == ["-O3"]

def test_bench_generator():
    config = Config(_repo_root / "tests" / "config.yaml")
    bench_generator = BenchGenerator(config=config, output_dir=_repo_root / "build" / "benchmarks", templates_path=_repo_root / "templates")
    bench_generator.generate()

def test_cmake_test_generator():
    config = Config(_repo_root / "tests" / "config.yaml")
    bench_generator = BenchGenerator(config=config, output_dir=_repo_root / "build" / "benchmarks", templates_path=_repo_root / "templates")
    benchmarks = bench_generator.generate()
    test_generator =  TestGenerator(config=config, build_path=_repo_root / "build", benchmarks=benchmarks)
    test_generator.generate()

def test_compare():
    config = Config(_repo_root / "tests" / "config.yaml")
    bench_generator = BenchGenerator(config=config, output_dir=_repo_root / "build" / "benchmarks", templates_path=_repo_root / "templates")
    benchmarks = bench_generator.generate()
    test_generator =  TestGenerator(config=config, build_path=_repo_root / "build", benchmarks=benchmarks)
    test_generator.generate()
    results_analyzer = ResultsAnalyzer(config=config, tests=tests)
    results_analyzer.compare(algorithm="copy", policies=("seq", "par"), size=1000000, compiler="g++", container="std::vector", type="int")

def test_plot():
    config = Config(_repo_root / "tests" / "config.yaml")
    bench_generator = BenchGenerator(config=config, output_dir=_repo_root / "build" / "benchmarks", templates_path=_repo_root / "templates")
    benchmarks = bench_generator.generate()
    test_generator =  TestGenerator(config=config, build_path=_repo_root / "build", benchmarks=benchmarks)
    tests = test_generator.generate()
    results_analyzer = ResultsAnalyzer(config=config, tests=tests)
    results_analyzer.plot_all()





