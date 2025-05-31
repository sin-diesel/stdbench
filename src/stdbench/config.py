import yaml

from pathlib import Path

ProcessedConfig: dict[str, list[str]]

class Config:
    def __init__(self, path: Path) -> None:
        with open(self.path, "r") as file:
            self._config = yaml.safe_load(file)
        self._template = self._config["template"]
        self._benchmark_config = self._config["benchmark"]
        self._environment_config = self._config["environment"]

   @staticmethod
    def transpose(self, config: ProcessedConfig) -> list[dict[str, str]]:
        return [[{key: v} for v in value] for key, value in config.items()]

    @property
    def benchmark_config(self, transposed: bool = False) -> ProcessedConfig:
        return self._benchmark_config if not transposed else self.transpose(self._benchmark_config)

    @property
    def environment_config(self, transposed: bool = False) -> ProcessedConfig:
        return self._environment_config if not transposed else self.transpose(self._benchmark_config)


