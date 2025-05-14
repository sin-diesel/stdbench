import os
import yaml
import shutil

from itertools import product
from jinja2 import Environment, Template, FileSystemLoader
from pathlib import Path


CMAKE_ENV_VARS_TEMPLATE = """
set(COMPILER {})
set(COMPILER_OPTS {})
"""


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

        if self._output_dir.exists():
            shutil.rmtree(self._output_dir)
        os.mkdir(self._output_dir)

    def _generate_env(self, config: dict[str, str | list[str]]) -> None:
        compilers = " ".join(config["compiler"])
        compiler_opts = " ".join(config["compiler_opts"])
        env_vars_path = self._output_dir / "cmake_env_vars.cmake"

        env_vars_path.write_text(CMAKE_ENV_VARS_TEMPLATE.format(compilers, compiler_opts))
        del config["compiler"]
        del config["compiler_opts"]

    def generate(self) -> None:
        env = Environment(loader=FileSystemLoader(self._templates_path))

        with open(self._config_path, "r") as file:
            config = yaml.safe_load(file)

        template = env.get_template(config["template"])
        del config["template"]

        self._generate_env(config)

        subconfigs = []
        for key, value in config.items():
            subconfigs.append([{key: v} for v in value])

        for params in product(*subconfigs):
            params_dict = {}
            for field in params:
                params_dict.update(field)
            benchmark = Benchmark(params_dict)
            benchmark.generate(template=template, output_dir=self._output_dir)
