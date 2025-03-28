import logging
import re
import os
from typing import Any
from pathlib import Path
from dataclasses import dataclass

from stdbench.config import ARCH
from stdbench.config import EXECUTOR
from stdbench.bench_generator import BenchGenerator
from stdbench.bench_compiler import BenchCompiler
from stdbench.bench_runner import BenchRunner
from stdbench.benchmark import Benchmark

_logger = logging.Logger(__file__)


@dataclass
class Template:
    name: str
    path: Path


@dataclass
class BenchConfig:
    regex: str
    params: dict[str, Any]


class BenchFactory:
    def __init__(
        self,
        templates_path: Path,
        benchmarks_path: Path,
        executor: EXECUTOR = EXECUTOR.HOST,
        arch: ARCH = ARCH.X86_64,
        binaries_path: Path = Path.cwd() / "elf",
        configs=None,
        compiler_path=None,
    ) -> None:
        self._arch = arch
        self._executor = executor
        self._templates_path = templates_path
        self._benchmarks_path = benchmarks_path
        self._binaries_path = binaries_path
        self._configs = configs
        self._compiler_path = compiler_path

        self._benchmarks: list[Benchmark] = []

    def _get_templates(self) -> list[Template]:
        templates: list[Template] = []
        if not self._templates_path.exists():
            raise FileNotFoundError(f"{self._templates_path} is missing")

        template_files = os.listdir(self._templates_path)
        if len(template_files) == 0:
            raise RuntimeError(f"{self._templates_path} is empty")

        for template in template_files:
            templates.append(Template(name=template, path=self._templates_path / template))
        return templates

    def generate(self) -> None:
        templates = self._get_templates()
        for config in self._configs:
            filtered_templates = filter(
                lambda template: re.search(config.regex, template.name),
                templates,
            )
            for template in filtered_templates:
                bench_generator = BenchGenerator(
                    template_file=template.path,
                    artifacts_folder=self._benchmarks_path,
                    params=config.params,
                )
                bench_name = bench_generator.generate()
                self._benchmarks.append(
                    Benchmark(
                        source_path=self._benchmarks_path / f"{bench_name}.cpp",
                        binary_path=self._binaries_path / f"{bench_name}.elf",
                    )
                )

    def compile(self) -> None:
        # Refactor it later
        compiler_path = os.environ["CXX"]
        for benchmark in self._benchmarks:
            bench_compiler = BenchCompiler(compiler_path=compiler_path, benchmark=benchmark)
            bench_compiler.compile()

    def run(self) -> None:
        for benchmark in self._benchmarks:
            bench_runner = BenchRunner(benchmark)
            bench_runner.run()
