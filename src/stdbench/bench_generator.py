import os
import yaml
import shutil
import copy

from itertools import product
from dataclasses import asdict
from jinja2 import Environment, Template, FileSystemLoader
from pathlib import Path

from stdbench.config import Config


class BenchmarkSource:
    def __init__(self, *, name: str, policy: Policy, input: Input, signature: str, output_dir: Path) -> None:
        self._name = name
        self._policy = policy
        self._input = input
        self._signature = signature
        self._output_dir = output_dir

    @property
    def name(self) -> str:
        return self._name

    @property
    def algorithm_name(self) -> str:
        return self._algorithm_name

    def generate(self) -> None:
        forbidden_characters = ["{", "}", "[", "]", "(", ")", ";", ":", "=", "&"]
        bench_name = ("_".join(self._params.values())).replace(" ", "_")
        bench_name = bench_name.translate({ord(char): "_" for char in forbidden_characters})
        bench_name = bench_name.replace("%", "div")
        bench_name = bench_name.replace("+", "plus")

        benchmark_path = self._output_dir / f"{bench_name}.cpp"
        benchmark_path.write_text(self._template.render(**self._params))


class CMakeHints:
    def __init__(self, path: Path) -> None:
        self._hints: list[tuple[str, str]] = []
        self._path = path

    def add(self, var: str, value: str) -> None:
        if not isinstance(var, str) or not isinstance(value, list):
            raise ValueError("Incorrect config, all keys must be str, all values must be lists")
        self._hints.append((var, value))

    def generate(self) -> None:
        hints_text = "".join([f"SET(\"{hint[0]}\" {' '.join(hint[1])})\n" for hint in self._hints])
        self._path.write_text(hints_text)


class BenchGenerator:
    def __init__(self, *, config: Config, output_dir: Path, templates_path: Path) -> None:
        self._config = config
        if output_dir.exists():
            shutil.rmtree(output_dir)
            os.mkdir(output_dir)
        self._output_dir = output_dir

        self._templates_path = templates_path

        self._env = Environment(loader=FileSystemLoader(self._templates_path))

    def _generate_cmake_hints(self) -> None:
        cmake_hints = CMakeHints(path=self._output_dir / "hints.cmake")
        for var, value in self._config.environment_config().items():
            cmake_hints.add(var=var, value=value)
        cmake_hints.generate()

    def generate(self) -> list[Benchmark]:
        for benchmark_config in self._config.benchmark_configs:
            breakpoint()
            transposed_bench_configs = Config.transpose(benchmark_config.algorithm_config())
            benchmarks_product = list(product(*transposed_bench_configs))

            benchmarks: list[Benchmark] = []
            for constructed_config in cartesian_product:
                params = self._config.normalize(config)
                benchmark = Benchmark(template=self._template, output_dir=self._output_dir, params=params)
                benchmark.generate()
                benchmarks.append(benchmark)

                self._generate_cmake_hints()

        return benchmarks
