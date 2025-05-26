import os
import json

from Gnuplot import Gnuplot
from Gnuplot import PlotItems
from glob import glob
from pathlib import Path
from dataclasses import asdict

from stdbench.benchmark import Measurement
from stdbench.benchmark import Benchmark


class Plotter:
    def __init__(self, build_folder: Path) -> None:
        self._build_folder = build_folder
        self._measurements = self._obtain_performance_measurements(build_folder, "clang++-19")
        self._gp = Gnuplot.Gnuplot()
        self._gp('set xlabel "size"')
        self._gp('set ylabel "cpu_time"')
        self._gp("set grid")

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
                    size=params["size"],
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
        print(measurements)

        # plot_item = PlotItems.Data(x, y, with_="lines", title="test")
        # self._gp.plot(plot_item)

        self._gp.hardcopy("output.png", terminal="png")
