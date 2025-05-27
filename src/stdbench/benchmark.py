import os
import yaml
import shutil
import copy

from itertools import product
from jinja2 import Environment, Template, FileSystemLoader
from dataclasses import dataclass
from pathlib import Path


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
    def __init__(self, params) -> None:
        self._params = params

    def generate(self, template: Template, output_dir: Path) -> None:
        forbidden_characters = ["{", "}", "[", "]", "(", ")", ";", ":", "="]
        bench_name = ("_".join(self._params.values())).replace(" ", "_")
        bench_name = bench_name.translate({ord(char): "_" for char in forbidden_characters})
        bench_name = bench_name.replace("%", "div")
        bench_name = bench_name.replace("+", "plus")

        benchmark_path = output_dir / f"{bench_name}.cpp"
        benchmark_path.write_text(template.render(**self._params))


class BenchGenerator:
    def __init__(self, config_path: Path, templates_path: Path, output_dir=Path("build") / "benchmarks") -> None:
        self._config_path = config_path
        self._templates_path = templates_path
        self._output_dir = output_dir
        self._subconfigs = []

        if self._output_dir.exists():
            shutil.rmtree(self._output_dir)
        os.mkdir(self._output_dir)

        self._env = Environment(loader=FileSystemLoader(self._templates_path))

        with open(self._config_path, "r") as file:
            self._config = yaml.safe_load(file)

    def _generate_env(self, config: dict[str, str | list[str]]) -> None:
        compiler_opts = " ".join(config["compiler_opts"])
        env_vars_path = self._output_dir / "compiler_opts.cmake"

        env_vars_path.write_text(CMAKE_ENV_VARS_TEMPLATE.format(compiler_opts))
        del config["compiler_opts"]

    def benchmark_names(self) -> list[str]:
        return self._config["name"]

    def benchmark_configs(self) -> list[dict]:
        return self._benchmark_configs

    def generate(self) -> list[Benchmark]:
        benchmarks: list[Benchmark] = []
        template = self._env.get_template(self._config["template"])
        del self._config["template"]

        self._generate_env(self._config)

        subconfigs = []
        for key, value in self._config.items():
            subconfigs.append([{key: v} for v in value])

        benchmark_config = copy.deepcopy(self._config)
        benchmark_configs = []
        del benchmark_config["size"]

        for key, value in benchmark_config.items():
            benchmark_configs.append([{key: v} for v in value])

        self._benchmark_configs = list(product(*benchmark_configs))

        self._subconfigs = list(product(*subconfigs))

        for params in self._subconfigs:
            params_dict = {}
            for field in params:
                params_dict.update(field)
            benchmark = Benchmark(params_dict)
            benchmark.generate(template=template, output_dir=self._output_dir)
            benchmarks.append(benchmark)

        return benchmarks
