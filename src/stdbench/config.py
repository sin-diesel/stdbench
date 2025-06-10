import yaml

from pathlib import Path

from stdbench.benchmark import BenchmarkConfig, Policy, Input


class Config:
    def __init__(self, path: Path) -> None:
        with open(path, "r") as file:
            self._config = yaml.safe_load(file)
        self._benchmark_configs = self._resolve_overrides(self._config)

    @staticmethod
    def _resolve_overrides(config: dict[str, list[str] | str]) -> list[BenchmarkConfig]:
        benchmark_configs: list[BenchmarkConfig] = []
        policy = [Policy[policy] for policy in config["benchmarks"]["policy"]]
        input = [Input[input] for input in config["benchmarks"]["input"]]
        environment = config["benchmarks"]["environment"]
        container = config["benchmarks"]["container"]
        type = config["benchmarks"]["type"]
        return_val = config["benchmarks"]["return"]

        for algorithm in config["benchmarks"]["algorithms"]:
            if algorithm.get("override", None):
                policy = algorithm["override"].get("policy", policy)
                input = algorithm["override"].get("input", input)
                container = algorithm["override"].get("container", container)
                environment = algorithm["override"].get("environment", environment)
                type = algorithm["override"].get("type", type)
                return_val = algorithm["override"].get("return", return_val)

            benchmark_configs.append(
                BenchmarkConfig(
                    name=algorithm["name"],
                    policy=policy,
                    input=input,
                    container=container,
                    type=type,
                    signature=algorithm["signature"],
                    return_val=return_val,
                    environment=environment,
                )
            )
        return benchmark_configs

    @staticmethod
    def transpose(config: dict[str, list[str]]) -> set[dict[str, str]] | list[dict[str, str]]:
        return [[{key: v} for v in value] for key, value in config.items()]

    @staticmethod
    def normalize(config: set[dict[str, str]] | list[dict[str, str]]) -> dict[str, list[str]]:
        return {list(value.keys())[0]: list(value.values())[0] for value in config}

    @property
    def benchmark_configs(self) -> list[BenchmarkConfig]:
        return self._benchmark_configs
