#!/usr/bin/env python3

import os
import subprocess
import logging

from pathlib import Path

from stdbench.utils import repo_root
from stdbench.benchmark import Benchmark

_logger = logging.getLogger(__file__)


class BenchCompiler:
    def __init__(self, compiler_path: Path, benchmark: Benchmark) -> None:
        self._compiler_path = compiler_path
        self._benchmark = benchmark

    def _find_benchmarks(self) -> list[Benchmark]:
        benchmarks: list[Benchmark] = []

        _logger.debug(f"Discovering benchmarks in {self._benchmarks_folder}")
        for file in os.listdir(self._benchmarks_folder):
            if file.endswith(".cpp"):
                _logger.debug(f"Found benchmark candidate: {file}")
                benchmarks.append(Benchmark(self._benchmarks_folder / file))

        return benchmarks

    def compile(self) -> None:
        if not self._benchmark.binary_path.parent.exists():
            os.makedirs(self._benchmark.binary_path.parent)

        cmd = [self._compiler_path, self._benchmark.source_path]
        if _logger.getEffectiveLevel() <= logging.DEBUG:
            cmd.append("--verbose")
        cmd = [
            self._compiler_path,
            self._benchmark.source_path,
            "-o",
            self._benchmark.binary_path,
        ]
        _logger.info(f"[started] Compiling {self._benchmark.source_path}")
        _logger.debug(f"Running command: {cmd} ")
        subprocess.run(cmd, check=True)
        _logger.info(
            f"[finished] Compiling {self._benchmark.source_path}: done"
        )
