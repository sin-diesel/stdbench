import os

from pathlib import Path
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self) -> None:
        pass

    def _obtain_performance_measurements(output_folder: Path) -> None:
        for measurement in os.listdir(output_folder):


