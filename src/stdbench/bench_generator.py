#!/usr/bin/env python3

from os.path import isdir
from os import makedirs

from pathlib import Path

from stdbench.utils import repo_root


class BenchGenerator:
    def __init__(
        self,
        params: dict[str, str],
        template_file: Path,
        artifacts_folder=repo_root / "generated",
    ) -> None:
        self._params = params
        self._template_file = template_file
        self._artifacts_folder = artifacts_folder

        if self._artifacts_folder.exists() and isdir(self._artifacts_folder):
            return

        makedirs(self._artifacts_folder)

    def _generate_output_name(self, template_path: Path) -> None:
        return Path(template_path.stem).with_suffix(".cpp")

    def generate(self) -> None:
        with open(self._template_file, "r") as file:
            contents = file.read()

        output_file = self._artifacts_folder / self._generate_output_name(
            self._template_file
        )

        with open(output_file, "w") as fout:
            fout.write(contents.format(**self._params))

