#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Benchmark:
    source_path: Path
    binary_path: Path
