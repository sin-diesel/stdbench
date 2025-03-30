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

    def compile(self) -> None:
        if not self._benchmark.binary_path.parent.exists():
            os.makedirs(self._benchmark.binary_path.parent)
        cmd = ["cmake", "--build", "build", "--target", self._benchmark.name]
