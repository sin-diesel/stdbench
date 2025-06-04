#!/usr/bin/env python3

from pathlib import Path

from stdbench.config import Config
from stdbench.bench_generator import BenchGenerator
from stdbench.test_generator import TestGenerator

_repo_root = Path(__file__).parent.parent.parent


def _main() -> None:
    config = Config(_repo_root / "tests" / "config.yaml")
    bench_generator = BenchGenerator(
        config=config, output_dir=_repo_root / "build" / "benchmarks", templates_path=_repo_root / "templates"
    )
    benchmarks = bench_generator.generate()

    test_generator = TestGenerator(config=config, build_path=_repo_root / "build", benchmarks=benchmarks)
    test_generator.generate()


if __name__ == "__main__":
    _main()
