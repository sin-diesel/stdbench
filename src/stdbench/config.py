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

        for algorithm in config["benchmarks"]["algorithms"]:
            if algorithm.get("override", None):
                policy = algorithm["override"].get("policy", policy)
                input = algorithm["override"].get("input", input)
                environment = algorithm["override"].get("environment", environment)

            benchmark_configs.append(
                BenchmarkConfig(
                    name=algorithm["name"],
                    policy=policy,
                    input=input,
                    signature=algorithm["signature"],
                    environment=environment,
                )
            )
        return benchmark_configs

    @property
    def benchmark_configs(self) -> list[BenchmarkConfig]:
        return self._benchmark_configs
