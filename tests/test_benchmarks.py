from pathlib import Path

from stdbench.benchmark import Benchmark, BenchGenerator

_repo_root = Path(__file__).parent.parent

def test_benchmarks_config():
    config_path = _repo_root / "tests" / "config.yaml"
    benchmarks = BenchGenerator(config_path, templates_path=_repo_root / "templates")
    benchmarks.generate()
