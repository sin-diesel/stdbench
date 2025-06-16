import os
import yaml
import shutil
import copy

from itertools import product
from dataclasses import asdict
from jinja2 import Environment, Template, FileSystemLoader
from pathlib import Path

from stdbench.config import Config
from stdbench.benchmark import Policy


class BenchmarkSource:
    def __init__(
        self,
        *,
        name: str,
        policy: Policy,
        input: str,
        signature: str,
        output_dir: Path,
        template: Template,
        container: str,
        type: str,
        return_val: str,
    ) -> None:
        self._name = name
        self._policy = policy
        self._input = input
        self._signature = signature
        self._output_dir = output_dir
        self._template = template
        self._container = container
        self._type = type
        self._return = return_val

    @property
    def name(self) -> str:
        return self._name

    @property
    def algorithm_name(self) -> str:
        return self._name

    def generate(self) -> None:
        forbidden_characters = ["\"", "/", "{", "}", "[", "]", "(", ")", ";", ":", "=", "&", "<", ">", ",", ".", "*"]
        bench_name = (
            "_".join([self._name, str(self._policy), self._input, self._container, self._type, self._signature])
        ).replace(" ", "_")
        bench_name = bench_name.translate({ord(char): "_" for char in forbidden_characters})
        bench_name = bench_name.replace("%", "div")
        bench_name = bench_name.replace("+", "plus")
        self._executable_name = bench_name

        benchmark_path = self._output_dir / f"{bench_name}.cpp"

        benchmark_path.write_text(
            self._template.render(
                name=self._name,
                container=self._container,
                type=self._type,
                signature=self._signature,
                policy=str(self._policy),
                input=self._input,
                return_val=self._return,
            )
        )


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
        self._template = self._env.get_template("algorithm_benchmark.jinja")

    def generate(self) -> list[BenchmarkSource]:
        benchmarks: list[BenchmarkSource] = []
        for benchmark_config in self._config.benchmark_configs:
            transposed_bench_configs = Config.transpose(benchmark_config.algorithm_config())
            benchmarks_product = list(product(*transposed_bench_configs))

            for transposed_config in benchmarks_product:
                normalized_config = Config.normalize(transposed_config)
                benchmark = BenchmarkSource(
                    name=normalized_config["name"],
                    policy=normalized_config["policy"],
                    input=normalized_config["input"],
                    signature=normalized_config["signature"],
                    container=normalized_config["container"],
                    type=normalized_config["type"],
                    return_val=normalized_config["return_val"],
                    output_dir=self._output_dir,
                    template=self._template,
                )
                benchmark.generate()
                benchmarks.append(benchmark)

        self._config.generate_cmake_hints(self._output_dir)
        return benchmarks
