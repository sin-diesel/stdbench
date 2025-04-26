import os
from envyaml import EnvYAML
from jinja2 import Environment
from pathlib import Path


class Benchmark:
    def __init__(self, *, name: str, env: Environment, template: str, output_dir: Path) -> None:
        self._env = env
        self._template = env.get_template(template)
        self._output_dir = output_dir
        self._name = name

    def generate(self, **params: str) -> None:
        os.makedirs(self._output_dir, exist_ok=True)
        benchmark_path = self._output_dir / f"{self._name}.cpp"
        benchmark_path.write_text(self._template.render(name=self._name, **params))

class BenchGenerator:
    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path

    def generate(self) -> None:
        contents = EnvYAML(self._config_path)
        breakpoint()
