import os
import json
import gnuplotlib as gp
import numpy as np

from glob import glob
from pathlib import Path
from dataclasses import asdict
from itertools import product

from stdbench.bench_generator import Benchmark
from stdbench.test_generator import CMakeTestTarget
from stdbench.config import Config


class ResultsAnalyzer:
    def __init__(self, *, config: Config, tests: list[CMakeTestTarget]) -> None:
        self._config = config
        self._tests = tests
        for test in self._tests:
            test.collect_measurements()

    def plot_all(self) -> None:
        benchmark_config = self._config.benchmark_config()
        environment_config = self._config.environment_config()
        test_config = benchmark_config | environment_config

        plot_keys = ["compiler", "compiler_opts", "container", "type", "name"]
        plot_configurations = {k: v for k, v in test_config.items() if k in plot_keys}

        cartesian_product = list(product(*Config.transpose(plot_configurations)))

        for plot_config in cartesian_product:
            plot_params = Config.normalize(plot_config)
            plots = []
            for policy in benchmark_config["policy"]:
                policy_plot_params = plot_params.copy()
                policy_plot_params.update({"policy": policy})
                tests = [
                    test
                    for test in self._tests
                    if all([getattr(test, param) == policy_plot_params[param] for param in policy_plot_params.keys()])
                ]

                x = np.array([int(test.size) for test in tests])
                y = np.array([float(test.cpu_time) for test in tests])
                x = np.log10(x)
                idx = np.argsort(x)
                x_s = x[idx]
                y_s = y[idx]

                plots.append((x_s, y_s, {"legend": policy}))
            gp_instance = gp.gnuplotlib()
            gp_instance.plot(
                *plots,
                title=f"name: {plot_params['name']}, \
compiler: {plot_params['compiler']}, \
compiler opts: {plot_params['compiler_opts']}, \
container: {plot_params['container']}, \
type: {plot_params['type']}",
                xlabel="log(size), n",
                ylabel="cpu_time, ns",
            )
