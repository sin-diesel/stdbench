import os
import yaml
from itertools import product
from jinja2 import Environment, Template, FileSystemLoader
from pathlib import Path


class Benchmark:
    def __init__(self, params) -> None:
        self._params = params

    def generate(self, template: Template, output_dir: Path) -> None:
        os.makedirs(output_dir, exist_ok=True)
        benchmark_path = output_dir / f"{self._params['name']}.cpp"
        benchmark_path.write_text(template.render(**self._params))


class BenchGenerator:
    def __init__(self, config_path: Path, templates_path: Path) -> None:
        self._config_path = config_path
        self._templates_path = templates_path

    def generate(self) -> None:
        env = Environment(loader=FileSystemLoader(self._templates_path))

        with open(self._config_path, "r") as file:
            contents = yaml.safe_load(file)

        template = env.get_template(contents["template"])
        del contents["template"]

        configs = []
        for key, value in contents.items():
            configs.append([{key: v} for v in value])

        for params in product(*configs):
            params_dict = {}
            for field in params:
                params_dict.update(field)
            benchmark = Benchmark(params_dict)
            benchmark.generate(template=template, output_dir=Path("benchmarks"))
