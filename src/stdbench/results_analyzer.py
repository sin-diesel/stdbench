import os
import json
import gnuplotlib as gp
import numpy as np

from glob import glob
from pathlib import Path
from dataclasses import asdict

from stdbench.bench_generator import Benchmark
from stdbench.test_generator import CMakeTestTarget
from stdbench.config import Config


class ResultsAnalyzer:
    def __init__(self, tests: list[CMakeTestTarget]) -> None:
        self._tests = tests
        for test in self._tests:
            test.collect_measurements()

    def _plot_data(
        self, *, name: str, T: str, src_container: str, policy: str, func: str, compiler: str, compiler_opts: str
    ):
        measurements = [
            measurement
            for measurement in self._measurements
            if measurement.name == name
            and measurement.T == T
            and measurement.src_container == src_container
            and measurement.func == func
            and measurement.compiler == compiler
            and measurement.compiler_opts == compiler_opts
            and measurement.policy == policy
        ]
        x = np.array([measurement.size for measurement in measurements])
        y = np.array([measurement.cpu_time for measurement in measurements])
        idx = np.argsort(x)
        x_s = x[idx]
        y_s = y[idx]

        return x_s, y_s

    def plot(
        self, *, name: str, T: str, src_container: str, policy: str, func: str, compiler: str, compiler_opts: str
    ) -> None:
        measurements = [
            measurement
            for measurement in self._measurements
            if measurement.name == name
            and measurement.T == T
            and measurement.src_container == src_container
            and measurement.func == func
            and measurement.compiler == compiler
            and measurement.compiler_opts == compiler_opts
            and measurement.policy == policy
        ]
        x = np.array([measurement.size for measurement in measurements])
        y = np.array([measurement.cpu_time for measurement in measurements])
        idx = np.argsort(x)
        x_s = x[idx]
        y_s = y[idx]

        gp.plot(
            (x_s, y_s, {"with": "linespoints"}), title=f"compiler: {compiler}", xlabel="size, n", ylabel="cpu_time, ns"
        )

    def plot_all(self, configs: list[dict]) -> None:
        compilers = ["clang++-19"]
        compiler_opts = ["-O2"]
        compiler = compilers[0]
        opts = compiler_opts[0]
        plots: list[tuple] = []
        # name = ""
        for config in configs:
            values = {list(mapping.keys())[0]: list(mapping.values())[0] for mapping in config}
            x, y = self._plot_data(
                name=values["name"],
                T=values["T"],
                src_container=values["src_container"],
                policy=values["policy"],
                func=values["func"],
                compiler=compiler,
                compiler_opts=opts,
            )
            policy = values["policy"]
            # name = values["name"]
            # underscore_idx = policy.index("_")
            # raw_policy = policy[:underscore_idx] + "\\" + policy[underscore_idx:]
            plots.append((x, y, {"legend": policy.replace("_", "-")}))

        gp.plot(
            *plots,
            title=f"name: count_if, compiler: {compiler}, compiler opts: -O2",
            xlabel="size, n",
            ylabel="cpu_time, ns",
        )
