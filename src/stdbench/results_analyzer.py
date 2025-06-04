import os
import json
import gnuplotlib as gp
import numpy as np

from glob import glob
from pathlib import Path
from dataclasses import asdict

from stdbench.bench_generator import Benchmark
from stdbench.test_generator import CMakeTestTarget
from stdbench.config import Config


class ResultsAnalyzer:
    def __init__(self, tests: list[CMakeTestTarget]) -> None:
        self._tests = tests
        for test in self._tests:
            test.collect_measurements()
