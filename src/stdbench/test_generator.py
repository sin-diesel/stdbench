from pathlib import Path

from stdbench.benchmark import Benchmark
from stdbench.test_target import TestTarget

class TestGenerator:
    def __init__(self, *, config_path: Path, output_dir: Path, benchmarks: list[Benchmark]) -> None:
        self._config = Config(config_path)
        if not output_dir.exists():
            os.mkdir(output_dir)
        self._output_dir = output_dir

        self._benchmarks = benchmarks

    def generate(self) -> list[TestTarget]:
        transposed_environment_configs = self._config.environment_config(transposed=True)
        cartesian_product = list(product(*transposed_environment_configs))

        tests: list[TestTarget] = []
        for config in cartesian_product:
            params = self._config.normalize(config)
            test = TestTarget()

