import logging
import re
import os
from typing import Any
from pathlib import Path
from dataclasses import dataclass

from stdbench.config import ARCH
from stdbench.config import EXECUTOR
from stdbench.bench_generator import BenchGenerator
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
        configs=None
    ) -> None:
        self._arch = arch
        self._executor = executor
        self._templates_path = templates_path
        self._benchmarks_path = benchmarks_path
        self._binaries_path = binaries_path
        self._configs = configs

        self._benchmarks: list[Benchmark] = []

    def _get_templates(self) -> list[Template]:
        templates: list[Template] = []
        if not self._templates_path.exists():
            raise FileNotFoundError(f"{self._templates_path} is missing")

        template_files = os.listdir(self._templates_path)
        if len(template_files) == 0:
            raise RuntimeError(f"{self._templates_path} is empty")

        for template in template_files:
            _logger.debug(f"Found template {self._templates_path / template}")
            templates.append(Template(name=template, path=self._templates_path / template))
        return templates

    def generate(self) -> None:
        templates = self._get_templates()
        for config in self._configs:
            filtered_templates = filter(lambda template: re.search(config.regex, template.name), templates)
            for template in filtered_templates:
                _logger.debug(f"Creating benchmark from template {template}, params: {config.params}")
                bench_generator = BenchGenerator(template_file=template.path, artifacts_folder=self._benchmarks_path, params=config.params)

                bench_name = bench_generator.generate()
                self._benchmarks.append(Benchmark(source_path=self._benchmarks_path / f"{bench_name}.cpp", binary_path = self._binaries_path / f"{bench_name}.elf" ))

    def compile(self) -> None:
        pass
