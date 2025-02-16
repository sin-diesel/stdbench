
from pathlib import Path

from stdbench.bench_generator import BenchGenerator

params = {
    "size": 10000,
    "type": "int",
    "transform_expression": "[](int x) { return x * 2; }",
    "policy": "par"
}

_repo_root = Path().parent.parent

template_file = _repo_root / "templates" / "transform.impl"


def test_generator() -> None:
    generator = BenchGenerator(params, template_file)
    generator.generate()

