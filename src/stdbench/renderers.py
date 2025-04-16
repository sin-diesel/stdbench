from abc import ABC, abstractmethod

from jinja2 import Template, Environment, DebugUndefined


class Renderer(ABC):
    def __init__(self) -> None:
        self._env = Environment(undefined=DebugUndefined)

    @abstractmethod
    def render(self, text: str) -> str:
        raise NotImplementedError


class BenchmarkRenderer(Renderer):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    def render(self, text: str) -> str:
        bench_name = self._name.replace("std::", "")
        function_signature = f"static void BM_{bench_name}(benchmark::State& state)"
        benchmark_register = f"BENCHMARK(BM_{bench_name});"
        main = "BENCHMARK_MAIN();"
        template = self._env.from_string(text)

        return template.render(
            name=self._name, function_signature=function_signature, benchmark_register=benchmark_register, main=main
        )


class ParPolicyRenderer(Renderer):
    def __init__(self) -> None:
        super().__init__()

    def render(self, text: str) -> str:
        template = self._env.from_string(text)
        return template.render(policy="std::execution::par,")


class InputDestRenderer(Renderer):
    def __init__(self, container: str = "std::vector<int>", size: int = 10000) -> None:
        super().__init__()
        self._container = container
        self._size = size

    def render(self, text: str) -> str:
        from_container = "test_from_container"
        dest_container = "test_dest_container"
        template = self._env.from_string(text)
        setup = f"""
{self._container} {from_container}({self._size});
std::iota({from_container}.begin(), {from_container}.end(), 0);
{self._container} {dest_container};
        """
        first = f"{from_container}.begin(),"
        last = f"{from_container}.end(),"
        d_first = f"std::back_inserter({dest_container}),"

        return template.render(setup=setup, first=first, last=last, d_first=d_first, size="", s_range="")


class SingleInputRenderer(Renderer):
    def __init__(self, container: str = "std::vector<int>", size: int = 10000) -> None:
        super().__init__()
        self._container = container
        self._size = size

    def render(self, text: str) -> str:
        from_container = "test_from_container"
        template = self._env.from_string(text)

        setup = f"""
{self._container} {from_container}({self._size});
std::iota({from_container}.begin(), {from_container}.end(), 0);
        """
        first = f"{from_container}.begin(),"
        last = f"{from_container}.end(),"

        return template.render(setup=setup, first=first, last=last, d_first="", size="", s_range="")


class SingleInputSizeRenderer(Renderer):
    def __init__(self, container: str = "std::vector<int>", size: int = 10000, n: int = 10) -> None:
        super().__init__()
        self._container = container
        self._size = size
        self._n = n

    def render(self, text: str) -> str:
        from_container = "test_from_container"
        template = self._env.from_string(text)

        setup = f"""
{self._container} {from_container}({self._size});
std::iota({from_container}.begin(), {from_container}.end(), 0);
        """
        first = f"{from_container}.begin(),"

        return template.render(setup=setup, first=first, last="", size=f"{self._n},", d_first="", s_range="")


class UnaryPredRenderer(Renderer):
    def __init__(self, pred: str = "[](int x) { return x % 3 == 0; }") -> None:
        super().__init__()
        self._pred = pred

    def render(self, text: str) -> str:
        template = self._env.from_string(text)
        return template.render(unary_pred=self._pred, binary_pred="")
