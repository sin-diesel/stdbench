import os
from jinja2 import Environment
from pathlib import Path


class Benchmark:
    def __init__(self, *, env: Environment, template: str, output_dir: Path) -> None:
        self._env = env
        self._template = env.get_template(template)
        self._output_dir = output_dir

    def generate(self, name: str, **params: str) -> None:
        os.makedirs(self._output_dir, exist_ok=True)
        benchmark_path = self._output_dir / f"{name}.cpp"
        benchmark_path.write_text(self._template.render(name=name, **params))
