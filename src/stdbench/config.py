import yaml

from pathlib import Path

NormalizedConfig = dict[str, list[str]]
TransposedConfig = set[dict[str, str]] | list[dict[str, str]]


class Config:
    def __init__(self, path: Path) -> None:
        with open(path, "r") as file:
            self._config = yaml.safe_load(file)
        self._template = self._config["template"]
        self._benchmark_config = self._config["benchmark"]
        self._environment_config = self._config["environment"]

    @property
    def template(self) -> str:
        return self._template

    @staticmethod
    def transpose(config: NormalizedConfig) -> TransposedConfig:
        return [[{key: v} for v in value] for key, value in config.items()]

    @staticmethod
    def normalize(config: TransposedConfig) -> NormalizedConfig:
        return {list(value.keys())[0]: list(value.values())[0] for value in config}

    def benchmark_config(self, transposed: bool = False) -> NormalizedConfig | TransposedConfig:
        return self._benchmark_config if not transposed else self.transpose(self._benchmark_config)

    def environment_config(self, transposed: bool = False) -> NormalizedConfig | TransposedConfig:
        return self._environment_config if not transposed else self.transpose(self._benchmark_config)
