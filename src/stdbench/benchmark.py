import os
import yaml
import shutil
import copy

from itertools import product
from jinja2 import Environment, Template, FileSystemLoader
from dataclasses import dataclass
from pathlib import Path

from stdbench.config import Config, NormalizedConfig


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
            template: str,
            output_dir: Path,
            params: NormalizedConfig
        ) -> None:
        self._template = template
        self._output_dir = output_dir
        self._params = params

    def generate(self) -> None:
        forbidden_characters = ["{", "}", "[", "]", "(", ")", ";", ":", "=", "&"]
        bench_name = ("_".join(self._params.values())).replace(" ", "_")
        bench_name = bench_name.translate({ord(char): "_" for char in forbidden_characters})
        bench_name = bench_name.replace("%", "div")
        bench_name = bench_name.replace("+", "plus")

        benchmark_path = self._output_dir / f"{bench_name}.cpp"
        benchmark_path.write_text(self._template.render(**self._params))


class BenchGenerator:
    def __init__(self, *, config_path: Path, output_dir: Path, templates_path: Path) -> None:
        self._config = Config(config_path)

        if not output_dir.exists():
            os.mkdir(output_dir)
        self._output_dir = output_dir

        self._templates_path = templates_path

        self._env = Environment(loader=FileSystemLoader(self._templates_path))
        self._template = self._env.get_template(self._config.template)


    def generate(self) -> list[Benchmark]:
        transposed_bench_configs = self._config.benchmark_config(transposed=True)
        cartesian_product = list(product(*transposed_bench_configs))

        benchmarks: list[Benchmark] = []
        for config in cartesian_product:
            params = self._config.normalize(config)
            benchmark = Benchmark(template=self._template, output_dir=self._output_dir, params=params)
            benchmark.generate()
            benchmarks.append(benchmark)

        return benchmarks
