
from conan import ConanFile
from conan.tools.cmake import cmake_layout


class StdBench(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("gcc/12.2.0")
        self.requires("benchmark/1.9.0")

    def layout(self):
        cmake_layout(self)
        self.folders.build = "build"
        self.folders.generators = "build"

