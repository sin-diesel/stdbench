#!/usr/bin/env python3

from Cheetah.Template import Template
from pathlib import Path


class CodeGenerator:
    def __init__(self, params: dict[str, str], template_file: Path) -> None:
        self._params = params
        self._template_file = template_file

    def _generate_output_name(self, template_name: Path) -> None:
        return template_name.stem.with_suffix(".cpp")

    def generate(self) -> None:
        with open(self._template, "r") as template_file:
            contents = template_file.read()

        generated_code = Template(contents, searchList=self._params)
        output_file = self._generate_output_name(self._template_file)

        with open(output_file, "w") as fout:
            fout.write(str(generated_code))

