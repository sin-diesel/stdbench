import os
import pytest
from pathlib import Path

from stdbench.benchmark import Benchmark, BenchGenerator

_repo_root = Path(__file__).parent.parent
_benchmarks_dir = _repo_root / "benchmarks"

@pytest.fixture()
def benchmarks_folder():
    os.makedirs(_benchmarks_dir, exist_ok=True)
    yield
    if _benchmarks_dir.exists():
        shutil.rmtree(_benchmarks_dir)

def test_benchmarks_config():
    config_path = _repo_root / "tests" / "config.yaml"
    benchmarks = BenchGenerator(config_path, templates_path=_repo_root / "templates")
    benchmarks.generate()
