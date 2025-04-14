from stdbench.algorithm import generate

template = \
"""
{{ function_signature }} {
 {{ setup }}

  {{ name }}({{ policy }} {{ range }} {{ size }} {{ s_range }} {{ d_first }} {{ unary_pred }} {{ binary_pred }});
}

{{ benchmark_register }};

{{ main }};
"""

def test_generate():
    generate(template, name="std::copy", policy="std::execution::par", container_name="my_container")

