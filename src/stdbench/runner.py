import re

from pathlib import Path

#
# class BenchRunner
#    def __init__(self, templates_path: Path) -> None:
#        self._templates: list[Template] = []
#
#    def discover_templates(self, templates_path: Path, pattern: str) -> list[str]:
#        regex = _re.compile(pattern)
#        names: list[str] = []
#        for template_name in os.listdir(template_path):
#            if not regex.search(pattern, template_name):
#                _logger.debug(f"Template {template_name} ignored")
#                continue
#
#            _logger.info(f"Adding template {template_name} to template list")
#            self._templates.append(Template(template_name))
#
#    @property
#    def templates(self) -> list[str]:
#        return [template.name for template in self._templates]
#
#    def config_templates(self) -> None:
#        if len(self._templates) == 0:
#            _logger.warning("Attempting to configure an empty list of templates")
#            return
#
#        for template in self._templates:
#            pass

#
#        _logger.debug(f"Discovering benchmarks in {self._benchmarks_folder}")
#        for file in os.listdir(self._benchmarks_folder):
#            if file.endswith(".cpp"):
#                _logger.debug(f"Found benchmark candidate: {file}")
#                benchmarks.append(Benchmark(self._benchmarks_folder / file))
#
#        return benchmarks
#
