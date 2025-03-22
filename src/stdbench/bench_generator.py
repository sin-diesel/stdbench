#!/usr/bin/env python3
import os
import logging

from pathlib import Path
from typing import Any

from stdbench.utils import repo_root

_logger = logging.getLogger(__file__)


class BenchGenerator:
    def __init__(
        self,
        params: dict[str, str],
        template_file: Path,
        artifacts_folder=Path,
    ) -> None:
        self._params = params
        self._template_file = template_file
        self._artifacts_folder = artifacts_folder

        if self._artifacts_folder.exists() and os.path.isdir(self._artifacts_folder):
            return

        os.makedirs(self._artifacts_folder)

    def _bench_name(self, template_file: Path, params: dict[str, Any]) -> str:
        params_str = "_".join([f"{item[0]}_{item[1]}" for item in params.items()])
        return f"{template_file.stem}_{params_str}"

    def generate(self) -> str:
        with open(self._template_file, "r") as file:
            contents = file.read()

        bench_name = self._bench_name(self._template_file, self._params)
        output_file = self._artifacts_folder / f"{bench_name}.cpp"

        with open(output_file, "w") as fout:
            _logger.info(f"[started] Generating sources to {output_file}")
            fout.write(contents.format(**self._params))
            _logger.info(f"[finished] Generating sources to {output_file}: done")

        return bench_name
