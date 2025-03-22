from stdbench.benchmark import Benchmark
import subprocess


class BenchRunner:
    def __init__(self, benchmark: Benchmark) -> None:
        self._benchmark = benchmark

    def run(self) -> None:
        cmd = ["time", self._benchmark.binary_path]
        time = subprocess.run(cmd, check=True, capture_output=True)
        print(time)
