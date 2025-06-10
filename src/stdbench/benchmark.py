from dataclasses import dataclass
from enum import Enum, auto


class Policy(Enum):
    seq = 1
    par = 2
    par_unseq = 3


class Input(Enum):
    random = auto()


@dataclass(kw_only=True)
class BenchmarkConfig:
    name: list[str]
    policy: list[Policy]
    input: list[Input]
    signature: list[str]
    environment: dict[str, list[str]]
