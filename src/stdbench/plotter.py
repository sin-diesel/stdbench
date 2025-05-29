import os
import json
import gnuplotlib as gp
import numpy as np

from glob import glob
from pathlib import Path
from dataclasses import asdict

from stdbench.benchmark import Measurement
from stdbench.benchmark import Benchmark


class Plotter:
    def __init__(self, build_folder: Path) -> None:
        self._build_folder = build_folder
        self._measurements = self._obtain_performance_measurements(build_folder, "clang++-19")

    @staticmethod
    def _obtain_performance_measurements(build_folder: Path, compiler: str) -> list[Measurement]:
        results = glob(str(build_folder / compiler / "*.json"))

        measurements: list[Measurement] = []
        for result in results:
            data = json.loads(Path(result).read_text())
            benchmark = data["benchmarks"][0]
            params = {
                key: data["context"][key]
                for key in ["name", "size", "T", "policy", "src_container", "func", "compiler", "compiler_opts"]
            }
            measurements.append(
                Measurement(
                    name=benchmark["name"],
                    T=params["T"],
                    policy=params["policy"],
                    size=int(params["size"]),
                    src_container=params["src_container"],
                    func=params["func"],
                    compiler=params["compiler"],
                    compiler_opts=params["compiler_opts"],
                    cpu_time=benchmark["cpu_time"],
                    real_time=benchmark["real_time"],
                    time_unit=benchmark["time_unit"],
                    iterations=benchmark["iterations"],
                )
            )

        return measurements

    def _plot_data(
        self, *, name: str, T: str, src_container: str, policy: str, func: str, compiler: str, compiler_opts: str
    ):
        breakpoint()
        measurements = [
            measurement
            for measurement in self._measurements
            if measurement.name == name and measurement.T == T and measurement.src_container == src_container and measurement.func == func and measurement.compiler == compiler and measurement.compiler_opts == compiler_opts and measurement.policy == policy
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
        name = ""
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
            name = values["name"]
            #underscore_idx = policy.index("_")
            #raw_policy = policy[:underscore_idx] + "\\" + policy[underscore_idx:]
            plots.append((x, y, {'legend': policy.replace("_", "-")}))

        gp.plot(
            *plots, title=f"name: count_if, compiler: {compiler}, compiler opts: -O2", xlabel="size, n", ylabel="cpu_time, ns"
        )

