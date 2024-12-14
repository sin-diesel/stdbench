
from codegen import CodeGenerator

params = {
    "type": "int",
    "values": "{1, 2, 3, 4, 5}",
    "transform_expression": "[](int x) { return x * 2; }",
    "transform_function": ""
}

template_file = "transform.impl"

generator = CodeGenerator(params, template_file)
generator.generate()

