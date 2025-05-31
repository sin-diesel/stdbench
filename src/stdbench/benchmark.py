import os
import yaml
import shutil
import copy

from itertools import product
from jinja2 import Environment, Template, FileSystemLoader
from dataclasses import dataclass
from pathlib import Path

from stdbench.config import Config, ProcessedConfig


CMAKE_ENV_VARS_TEMPLATE = """
set(COMPILER_OPTS {})
"""


@dataclass(kw_only=True)
class Measurement:
    name: str
    T: str
    policy: str
    size: str
    src_container: str
    func: str
    compiler: str
    compiler_opts: str

    time_unit: str
    cpu_time: float
    real_time: float
    iterations: int


class Benchmark:
    def __init__(
            self,
            *,
            template: Template,
            output_dir: Path,
            params: ProcessedConfig
        ) -> None:
        self._template = template
        self._output_dir = output_dir
        self._params = params

    def generate(self, template: Template, output_dir: Path) -> None:
        forbidden_characters = ["{", "}", "[", "]", "(", ")", ";", ":", "=", "&"]
        bench_name = ("_".join(self._params.values())).replace(" ", "_")
        bench_name = bench_name.translate({ord(char): "_" for char in forbidden_characters})
        bench_name = bench_name.replace("%", "div")
        bench_name = bench_name.replace("+", "plus")

        benchmark_path = output_dir / f"{bench_name}.cpp"
        benchmark_path.write_text(template.render(**self._params))


class BenchGenerator:
    def __init__(self, config_path: Path, output_dir: Path, templates_path: Path) -> None:
        self._config = Config(config_path)
        self._output_dir = output_dir
        self._templates_path = templates_path

        self._env = Environment(loader=FileSystemLoader(self._templates_path))

    def benchmark_names(self) -> list[str]:
        return self._config["name"]

    def benchmark_configs(self) -> list[dict]:
        return self._benchmark_configs

    def generate(self) -> list[Benchmark]:
        transposed_bench_configs = self._config.benchmark_config(transposed=True)
        cartesian_product = list(product(*transposed_bench_configs))

        benchmarks: list[Benchmark] = []
        for config in cartesian_product:
            params = {value for value in config}
            benchmark = Benchmark(template=self_config.template, output_dir=self._output_dir, params=params)
            benchmarks.append(benchmark)

        return benchmarks
