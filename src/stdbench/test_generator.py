import json

from pathlib import Path
from itertools import product

from stdbench.bench_generator import BenchmarkSource
from stdbench.config import Config


class CMakeTestTarget:
    def __init__(self, *, build_path: Path, benchmark: BenchmarkSource, env: dict[str, str]) -> None:
        self._compiler_opts = env["compiler_options"]
        self._size = env["size"]
        self._compiler = "g++"
        self._benchmark = benchmark

        self._executable_name = f"{benchmark._executable_name}_{self._compiler_opts}"
        self._name = f"{self._executable_name}_{self._size}"
        self._results_path = build_path / self._compiler / f"{self._name}.json"

        self._cpu_time: int | None = None
        self._time_unit: str | None = None
        self._iterations: int | None = None

    @property
    def compiler_options(self) -> str:
        return self._compiler_opts

    @property
    def compiler(self) -> str:
        return self._compiler

    @property
    def name(self) -> str:
        return self._benchmark.name

    @property
    def input(self) -> str:
        return self._benchmark._input

    @property
    def container(self) -> str:
        return self._benchmark._container

    @property
    def type(self) -> str:
        return self._benchmark._type

    @property
    def policy(self) -> str:
        return str(self._benchmark._policy)

    @property
    def cpu_time(self) -> int:
        return self._cpu_time

    @property
    def size(self) -> int:
        return self._size

    def collect_measurements(self) -> None:
        if not self._results_path.exists():
            raise FileNotFoundError("Benchmarks results were not found. Did you forget to run the tests?")
        data = json.loads(self._results_path.read_text())
        benchmark = data["benchmarks"][0]
        self._cpu_time = benchmark["cpu_time"]
        self._time_unit = benchmark["time_unit"]
        self._iterations = benchmark["iterations"]


class TestGenerator:
    def __init__(self, *, config: Config, build_path: Path, benchmarks: list[BenchmarkSource]) -> None:
        self._build_path = build_path
        self._benchmarks = benchmarks
        self._config = config

    def generate(self) -> list[CMakeTestTarget]:
        tests: list[CMakeTestTarget] = []
        for benchmark_config in self._config.benchmark_configs:
            transposed_env_configs = Config.transpose(benchmark_config.environment_config())
            benchmarks_product = list(product(*transposed_env_configs))
            for transposed_config in benchmarks_product:
                for benchmark in self._benchmarks:
                    params = Config.normalize(transposed_config)
                    test = CMakeTestTarget(build_path=self._build_path, benchmark=benchmark, env=params)
                    tests.append(test)
        return tests
