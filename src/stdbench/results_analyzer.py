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
      #  x = np.array([measurement.size for measurement in measurements])
      #  y = np.array([measurement.cpu_time for measurement in measurements])
      #  idx = np.argsort(x)
      #  x_s = x[idx]
      #  y_s = y[idx]

        env_config = self._config.environment_config()
        benchmark_config = self._config.benchmark_config()

        compilers = env_config["compiler"]
        compiler_opts = env_config["compiler_opts"]
        algorithms = benchmark_config["name"]

        plot_configurations = {k: v for k, v in (env_config | benchmark_config).items() if k in ["compiler", "compiler_opts", "name"]}

        cartesian_product = list(product(*Config.transpose(plot_configurations)))

        for configuration in cartesian_product:
            for policy in benchmark_config["policy"]:
                params = Config.normalize(configuration)
                breakpoint()
 #               tests = [test for test in self._tests if all([getattr(test, param) == params[param] for param in params.keys()])]
 #           x = np.array([test.size for test in tests])
 #           y = np.array([test.cpu_time for test in tests])
 #           idx = np.argsort(x)
 #           x_s = x[idx]
 #           y_s = y[idx]

 #           policy = values["policy"]
            # name = values["name"]
#            # underscore_idx = policy.index("_")
#            # raw_policy = policy[:underscore_idx] + "\\" + policy[underscore_idx:]
#            plots.append((x, y, {"legend": policy.replace("_", "-")}))

#       gp.plot(
 #           (x_s,  y_s, {"with": "linespoints"}), title=f"compiler: {params['compiler']}", xlabel="size, n", ylabel="cpu_time, ns"
 #       )
##
