import shutil
import os
from pathlib import Path

from stdbench.bench_generator import BenchGenerator
from stdbench.bench_compiler import BenchCompiler
from stdbench.benchmark import Benchmark
from stdbench.bench_factory import BenchFactory

params = {
    "size": 10000,
    "type": "int",
    "transform_expression": "[](int x) { return x * 2; }",
    "policy": "par"
}

_repo_root = Path().parent.parent

template_file = _repo_root / "templates" / "transform.impl"


def test_get_templates() -> None:
    bench_factory = BenchFactory(templates_path=_repo_root / "templates", benchmarks_path=_repo_root / "artifacts"  / "benchmarks")
    templates =  bench_factory._get_templates()
    assert templates is not None

def test_generator() -> None:
    generator = BenchGenerator(params=params, template_file=template_file, artifacts_folder=_repo_root / "sources")
    generator.generate()

def test_bench_compiler() -> None:
    compiler_path = os.environ["CXX"]
    assert "conan" in compiler_path

    compiler = BenchCompiler(compiler_path,
                             benchmark=Benchmark(source_path=_repo_root / "tests" / "benchmarks" / "transform.cpp",
                                                 binary_path=_repo_root / "tests" / "bin" / "transform.elf"))
    compiler.compile()

