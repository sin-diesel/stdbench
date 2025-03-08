#!/usr/bin/env python3

from utils import repo_root
from pathlib import Path


class Compiler:
    def __init__(
        self, compiler_path: Path, benchmarks_folder=repo_root / "generated"
    ) -> None:
        benchmarks_folder = repo_root / "generated"
