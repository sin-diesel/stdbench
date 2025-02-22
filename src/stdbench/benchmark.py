#!/usr/bin/env python3

from pathlib import Path


class Benchmark:
    def __init__(self, source_path: Path, binary_path: Path) -> None:
        self._source_path = source_path
        self._binary_path = binary_path

    @property
    def source_path(self) -> Path:
        return self._source_path

    @property
    def binary_path(self) -> Path:
        return self._binary_path
