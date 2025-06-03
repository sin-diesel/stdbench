from pathlib import Path
from itertools import product

from stdbench.bench_generator import Benchmark
from stdbench.config import Config

class CMakeTestTarget:
    def __init__(self, *, build_path: Path, benchmark: Benchmark, env: dict[str, str]) -> None:
        self._executable_name = benchmark.name
        self._compiler_opts = env["compiler_opts"]
        self._compiler = env["compiler"]
        self._size = env["size"]

        self._name = f"{self._executable_name}_{self._size}_{self._compiler_opts}"
        self._results_path = build_path / self._compiler / self._name


class TestGenerator:
    def __init__(self, *, config: Config, build_path: Path, benchmarks: list[Benchmark]) -> None:
        self._build_path = build_path
        self._benchmarks = benchmarks
        self._config = config

    def generate(self) -> list[CMakeTestTarget]:
        transposed_environment_configs = self._config.environment_config(transposed=True)
        cartesian_product = list(product(*transposed_environment_configs))

        tests: list[TestTarget] = []
        for config in cartesian_product:
            for benchmark in self._benchmarks:
                params = self._config.normalize(config)
                breakpoint()
                test = CMakeTestTarget(build_path=self._build_path, benchmark=benchmark, env=params)
                tests.append(test)
        return tests

