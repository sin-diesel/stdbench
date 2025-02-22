#!/usr/bin/env python3

from pathlib import Path

class Benchmark:
    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path
