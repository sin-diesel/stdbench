
from conan import ConanFile
from conan.tools.cmake import cmake_layout


class StdBench(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("gcc/12.2.0")
        self.requires("cppbenchmark/1.0.4.0")

    def layout(self):
        cmake_layout(self)

