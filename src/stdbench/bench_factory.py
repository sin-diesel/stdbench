import logging
import re
import os
from typing import Any
from pathlib import Path
from dataclasses import dataclass

from stdbench.config import ARCH
from stdbench.config import EXECUTOR
from stdbench.bench_generator import BenchGenerator

_logger = logging.Logger(__file__)


@dataclass
class Template:
    name: str
    path: Path


class BenchConfig:
    def __init__(self, regex: str, **template_params: dict[str, Any]) -> None:
        self._regex = re.compile(regex)
        self._template_params = template_params


class BenchFactory:
    def __init__(
        self,
        templates_path: Path,
        benchmarks_path: Path,
        executor: EXECUTOR = EXECUTOR.HOST,
        arch: ARCH = ARCH.X86_64,
        binaries_path: Path = Path.cwd() / "elf",
        configs=None,
    ) -> None:
        self._arch = arch
        self._executor = executor
        self._templates_path = templates_path
        self._benchmarks_path = benchmarks_path
        self._binaries_path = binaries_path
        self._configs = configs

    def _get_templates(self) -> list[Template]:
        templates: list[Template] = []
        if not self._templates_path.exists():
            raise FileNotFoundError(f"{self._templates_path} is missing")

        template_files = os.listdir(self._templates_path)
        if len(template_files) == 0:
            raise RuntimeError(f"{self._templates_path} is empty")

        for template in template_files:
            template_abspath = self._templates_path / "templates"
            _logger.debug(f"Found template {template_abspath}")
            templates.append(Template(name=template, path=template_abspath))
        return templates

