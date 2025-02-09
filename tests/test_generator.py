
from pathlib import Path

from stdbench.codegen import CodeGenerator

params = {
    "size": 10000,
    "type": "int",
    "transform_expression": "[](int x) { return x * 2; }"
}

_repo_root = Path().parent.parent

template_file = _repo_root / "templates" / "transform.impl"


def test_generator() -> None:
    generator = CodeGenerator(params, template_file)
    breakpoint()
    generator.generate()

