import os
import json
from glob import glob
from pathlib import Path
from dataclasses import asdict

from stdbench.benchmark import Measurement
from stdbench.benchmark import Benchmark


class Plotter:
    def __init__(self, build_folder: Path, benchmarks: list[Benchmark]) -> None:
        self._build_folder = build_folder
        self._benchmarks = benchmarks
        self._measurements = self._obtain_performance_measurements(build_folder, "g++")

    @staticmethod
    def _obtain_performance_measurements(build_folder: Path, compiler: str) -> list[Measurement]:
        results = glob(str(build_folder / compiler / "*.json"))

        measurements: list[Measurement] = []
        for result in results:
            data = json.loads(Path(result).read_text())
            benchmark = data["benchmarks"][0]
            measurements.append(Measurement(name=benchmark["name"], cpu_time=benchmark["cpu_time"], real_time=benchmark["real_time"], time_unit=benchmark["time_unit"], iterations=benchmark["iterations"]))

        return measurements

#    def _obtain_cpu_time(self, name: str, bench_params: dict[str, str]) -> list[float]:
#        cpu_time = [measurement.cpu_time for measurement in self._measurements if all(fixed_axes[axe] == asdict(measurement)[axe] for axe in fixed_axes.keys())]

        # gnuplot...




