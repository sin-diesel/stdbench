#!/usr/bin/env python3

import enum
import typing


class ARCH(enum.Enum):
    X86_64 = enum.auto()
    RISCV64 = enum.auto()


class EXECUTOR(enum.Enum):
    HOST = enum.auto()
    gem5 = enum.auto()


# class RunnerConfig:
#    def __init__(self, bench_config: BenchConfig) -> None:
#        self._bench_config = bench_config
#
#
# basic_bench_config = BenchConfig(
#    arch="x86_64",
#    executor="host",
#    template_params={
#        "size": int,
#        "type": str,
#        "transform_expression": str,
#        "policy": str,
#    },
# )
