import os
from os import path
import shutil

from distutils.cmd import Command
from distutils.command.build_ext import build_ext
from setuptools import setup


class CleanCommand(Command):
    description = 'Clean up /build and any compiled output in the main tree.'
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        if path.exists('./build'):
            shutil.rmtree('./build')

        # Walk the directory structure and get the files we care about
        built_files = []
        for root, dirs, files in os.walk("."):
            # Get all the py and pyx files for compiling
            for filename in files:
                if filename.endswith('.c') or filename.endswith('.so') or filename.endswith('.dll'):
                    os.unlink(path.join(root, filename))

            # Skip hidden directories and the build directory
            i = 0
            while i < len(dirs):
                if dirs[i][0] == '.' or (root == '.' and dirs[i] == 'build'):
                    del dirs[i]
                else:
                    i += 1


class CompileCommand(build_ext):
    description = 'Compile all Python & Cython files into .so or .dll files.'

    def run(self):
        # Inline imports because we need setuptools to install this module first
        from Cython.Build import cythonize
        from Cython.Build.Dependencies import create_extension_list

        source_files = create_extension_list(['**/*.pyx', '**/*.py'])[0]
        for f in source_files:
            f.extra_compile_args = [
                '-Wno-unneeded-internal-declaration',
                '-Wno-unused-function'
            ]
        self.extensions = cythonize(source_files)
        build_ext.run(self)


setup_options = setup(
    name=path.basename(path.realpath(__file__)),
    install_requires=[
        'cython >= 0.23.4'
    ],
    cmdclass={
        'clean': CleanCommand,
        'compile': CompileCommand
    }
)

