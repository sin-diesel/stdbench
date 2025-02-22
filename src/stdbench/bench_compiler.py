#!/usr/bin/env python3

from pathlib import Path
from logging import Logger
from os import listdir
from subprocess import run

from stdbench.utils import repo_root
from stdbench.benchmark import Benchmark

_logger = Logger(__file__)

class BenchCompiler:
    def __init__(self, compiler_path: Path, benchmarks_folder = repo_root / "generated") -> None:
        self._compiler_path = compiler_path
        self._benchmarks_folder = benchmarks_folder

    def _find_benchmarks(self) -> list[Benchmark]:
        benchmarks: list[Benchmark] = []

        _logger.debug(f"Discovering benchmarks in {self._benchmarks_folder}...")
        for file in listdir(self._benchmarks_folder):
            if file.endswith(".cpp"):
                _logger.debug(f"Found benchmark candidate: {file}")
                benchmarks.append(Benchmark(self._benchmarks_folder / file))

        return benchmarks

    def compile(self) -> None:
        benchmarks = self._find_benchmarks()
        for benchmark in benchmarks:
            cmd = [self._compiler_path, benchmark.path]
            run(cmd)

