from stdbench.renderers import Renderer


class Benchmark:
    def __init__(
        self,
        *,
        benchmark_renderer: Renderer,
        policy_renderer: Renderer,
        inputs_renderer: Renderer,
        predicate_renderer: Renderer,
    ) -> None:
        self._renderers = (benchmark_renderer, policy_renderer, inputs_renderer, predicate_renderer)

    def render(self) -> None:
        output: str = """
#include <algorithm>
#include <execution>
#include <numeric>

#include <benchmark/benchmark.h>

{{ function_signature }} {
 {{ setup }}

 for (auto _: state) {
   {{ name }}({{ policy }} {{ first }} {{ last }} {{ size }} {{ s_range }} {{ d_first }} {{ unary_pred }} {{ binary_pred }});
   }
}

{{ benchmark_register }};

{{ main }};
"""
        for renderer in self._renderers:
            output = renderer.render(output)
        return output
