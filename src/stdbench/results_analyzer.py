import os
import json
import gnuplotlib as gp
import numpy as np

from glob import glob
from pathlib import Path
from dataclasses import asdict
from itertools import product

from stdbench.test_generator import CMakeTestTarget
from stdbench.config import Config


class ResultsAnalyzer:
    def __init__(self, *, config: Config, tests: list[CMakeTestTarget]) -> None:
        self._config = config
        self._tests = tests
        for test in self._tests:
            test.collect_measurements()

    def compare(
        self,
        *,
        algorithm: str,
        policies: tuple[str, str],
        size: int,
        compiler: str,
        container: str,
        type: str
    ) -> float:
        policy_first = policies[0]
        tests_first = [test for test in self._tests if algorithm == test.name and policy_first == test.policy and compiler == test.compiler and container == test.container and type == test.type and size == test.size]
        execution_time_first = set([test.cpu_time for test in tests_first]).pop()

        policy_second = policies[1]
        tests_second = [test for test in self._tests if algorithm == test.name and policy_second == test.policy and compiler == test.compiler and container == test.container and type == test.type and size == test.size]

        execution_time_second = set([test.cpu_time for test in tests_second]).pop()
        return execution_time_first / execution_time_second

    def compare_all(
        self,
        *,
        policies: tuple[str, str],
        size: int,
        compiler: str,
        container: str,
        type: str
    ) -> list[tuple[str, float]]:
        algorithms = set([test.name for test in self._tests])
        ratios: list[tuple[str, float]] = []
        ratios = [(algorithm, self.compare(
            algorithm=algorithm,
            policies=policies,
            size=size,
            compiler=compiler,
            container=container,
            type=type
        )) for algorithm in algorithms]
        ratios = sorted(ratios, key=lambda value: value[1])
        breakpoint()


        gp_instance = gnuplotlib.Gnuplot()
        gp_instance('set yrange [1:*]') 

        gp_instance('''
            set style data histogram
            set style fill solid
            set boxwidth 0.8
            plot '-' using 2:xtic(1) with boxes title 'Data'
            "A" 5
            "B" 8
            "C" 3
            "D" 7
            "E" 6
            e
        '''
        )

    def plot_all(self) -> None:
        for benchmark_config in self._config.benchmark_configs:
            plot_keys = ["compiler", "compiler_options", "container", "type", "name", "input"]
            plot_configurations = {k: v for k, v in asdict(benchmark_config).items() if k in plot_keys}
            plot_configurations["compiler"] = ["g++"]
            plot_configurations["compiler_options"] = asdict(benchmark_config)["environment"]["compiler_options"]

            cartesian_product = list(product(*Config.transpose(plot_configurations)))

            for plot_config in cartesian_product:
                plot_params = Config.normalize(plot_config)
                plots = []
                for policy in asdict(benchmark_config)["policy"]:
                    policy = str(policy)
                    policy_plot_params = plot_params.copy()
                    policy_plot_params.update({"policy": policy})
                    tests = [
                        test
                        for test in self._tests
                        if all(
                            [getattr(test, param) == policy_plot_params[param] for param in policy_plot_params.keys()]
                        )
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
                    compiler opts: {plot_params['compiler_options']}, \
                    container: {plot_params['container']}, \
                    type: {plot_params['type']}",
                    xlabel="log(size), n",
                    ylabel="cpu_time, ns",
                )
