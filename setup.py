from setuptools import setup

from setuptools.command.build_py import build_py

from generate_grammar import generate_grammar


class CustomBuilder(build_py):
    def run(self):
        generate_grammar()
        super(CustomBuilder, self).run()


setup(cmdclass={'build_py': CustomBuilder})
