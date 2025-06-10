from pathlib import Path

from stdbench.config import Config

_repo_root = Path(__file__).parent.parent

def test_config():
    config = Config(_repo_root / "tests" / "config.yaml")
    assert config
    assert len(config.benchmark_configs) >  0
    assert config.benchmark_configs[0].name != ""

    assert config.benchmark_configs[0].environment["compiler_options"] == ["-O2"] or \
    config.benchmark_configs[0].environment["compiler_options"] == ["-O3"]

