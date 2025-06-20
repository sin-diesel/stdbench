import yaml

from pathlib import Path

from stdbench.benchmark import BenchmarkConfig, Policy


class _CMakeHints:
    def __init__(self, path: Path) -> None:
        self._hints: list[tuple[str, str]] = []
        self._path = path

    def add(self, var: str, value: str) -> None:
        if not isinstance(var, str) or not isinstance(value, list):
            raise ValueError("Incorrect config, all keys must be str, all values must be lists")
        self._hints.append((var, value))

    def generate(self) -> None:
        hints_text = "".join([f"SET(\"{hint[0]}\" {' '.join(hint[1])})\n" for hint in self._hints])
        self._path.write_text(hints_text)


class Config:
    def __init__(self, path: Path) -> None:
        with open(path, "r") as file:
            self._config = yaml.safe_load(file)
        self._benchmark_configs = self._resolve_overrides(self._config)

    def generate_cmake_hints(self, output_dir: Path) -> None:
        cmake_hints = _CMakeHints(path=output_dir / "hints.cmake")
        for var, value in self._config["benchmarks"]["environment"].items():
            cmake_hints.add(var=var, value=value)
        cmake_hints.generate()

    @staticmethod
    def _resolve_overrides(config: dict[str, list[str] | str]) -> list[BenchmarkConfig]:
        benchmark_configs: list[BenchmarkConfig] = []
        default_policy = [Policy[policy] for policy in config["benchmarks"]["policy"]]
        default_input = config["benchmarks"]["input"]
        default_environment = config["benchmarks"]["environment"]
        default_container = config["benchmarks"]["container"]
        default_type = config["benchmarks"]["type"]
        default_return_val = config["benchmarks"]["return"]

        policy = default_policy
        input = default_input
        container = default_container
        type = default_type
        return_val = default_return_val
        environment = default_environment

        for algorithm in config["benchmarks"]["algorithms"]:
            if algorithm.get("override", None):
                policy = algorithm["override"].get("policy", default_policy)
                input = algorithm["override"].get("input", default_input)
                container = algorithm["override"].get("container", default_container)
                environment = algorithm["override"].get("environment", default_environment)
                type = algorithm["override"].get("type", default_type)
                return_val = algorithm["override"].get("return", default_return_val)

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
