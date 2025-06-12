import os
import json
import gnuplotlib as gp
import numpy as np
import matplotlib.pyplot as plt

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
        self, *, algorithm: str, policies: tuple[str, str], size: int, compiler: str, container: str, type: str
    ) -> float:
        policy_first = policies[0]
        tests_first = [
            test
            for test in self._tests
            if algorithm == test.name
            and policy_first == test.policy
            and compiler == test.compiler
            and container == test.container
            and type == test.type
            and size == test.size
        ]
        execution_time_first = set([test.cpu_time for test in tests_first]).pop()

        policy_second = policies[1]
        tests_second = [
            test
            for test in self._tests
            if algorithm == test.name
            and policy_second == test.policy
            and compiler == test.compiler
            and container == test.container
            and type == test.type
            and size == test.size
        ]

        execution_time_second = set([test.cpu_time for test in tests_second]).pop()
        return execution_time_first / execution_time_second

    def compare_all(
        self, *, policies: tuple[str, str], size: int, compiler: str, container: str, type: str
    ) -> list[tuple[str, float]]:
        algorithms = set([test.name for test in self._tests])
        ratios: list[tuple[str, float]] = []
        ratios = [
            (
                algorithm,
                self.compare(
                    algorithm=algorithm, policies=policies, size=size, compiler=compiler, container=container, type=type
                ),
            )
            for algorithm in algorithms
        ]
        ratios = sorted(ratios, key=lambda value: value[1])
        names = [ratio[0] for ratio in ratios]
        speedups = [ratio[1] for ratio in ratios]
        breakpoint()

        fig, ax = plt.subplots(figsize=(8, 5))

        upwards = [v if v >= 1 else 0 for v in speedups]
        downwards = [1 - v if v < 1 else 0 for v in speedups]

        ax.bar(names, np.array(upwards), bottom=1, color="green", alpha=0.7, width=0.6, label="≥1")

        ax.bar(names, -np.array(downwards), bottom=1, color="red", alpha=0.7, width=0.6, label="<1")

        ax.axhline(y=1, color="black", linewidth=1.5, linestyle="-")  # Thick line at Y=1
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        ax.set_title(f"compiler = {compiler}, size={size}, policies: {policies[1]} / {policies[0]}", pad=20)
        ax.set_xlabel("algorithms")
        ax.set_ylabel(f"speedup, {policies[1]} / {policies[0]}")

        ax.axhspan(0, 1, color="lightgray", alpha=0.2, zorder=0)
        ax.axhline(y=1, color="black", linestyle="--", linewidth=0.8)

        ax.set_yticks([0, 0.2, 0.5, 1, 5, 10, 15])
        ax.set_yticklabels(["0", "0.2", "0.5", "1", "5", "10", "15"])

        ax.set_xticklabels(names, fontsize=5)  # Smaller category labels
        ax.set_ylim(0, max(speedups) + 1.5)  # Ensures Y=1 is visible

        plt.xticks(rotation=90)

        # for bar in bars:
        #    height = bar.get_height()
        #    ax.text(bar.get_x() + bar.get_width()/2.,
        #        height + 1.02,  # Position text above bar (1 + height + offset)
        #        f'{height}',
        #        ha='center',
        #        va='bottom')

        plt.tight_layout()
        plt.savefig("barplot.png")

    # x_positions = np.arange(len(names))

    # gp_instance = gp.gnuplotlib()
    # gp.plot(
    #     (x_positions, speedups, {'with': 'boxes'}),
    #     _yrange = [0, None],
    #     commands = [
    #         f"set xtics ({', '.join([f'{label} {i}' for i, label in enumerate(names)])})",
    #         'set arrow 1 from graph 0, first 1 to graph 1, first 1 nohead lw 2',
    #         'set grid y',
    #         'set style fill solid border',
    #         'unset key'  # Remove legend if not needed
    #     ],
    #     terminal = 'qt',
    #     title = 'Bar plot with X-axis at Y=1',
    #     xlabel = 'algorithms',
    #     ylabel = 'speedup'
    # )

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
