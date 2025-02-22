
import shutil
import os
from pathlib import Path

from stdbench.bench_generator import BenchGenerator
from stdbench.bench_compiler import BenchCompiler

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

def test_bench_compiler() -> None:
    shutil.rmtree(_repo_root / "generated")

    generator = BenchGenerator(params, template_file)
    generator.generate()

    compiler_path = os.environ["CC"]
    assert "conan" in compiler_path
    breakpoint()

    compiler = BenchCompiler(compiler_path, benchmarks_folder = _repo_root / "tests" / "benchmarks")
    compiler.compile()

