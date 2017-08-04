#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import os
from setuptools import setup, find_packages


local_file = lambda *f: \
    open(os.path.join(os.path.dirname(__file__), *f)).read()


class VersionFinder(ast.NodeVisitor):
    VARIABLE_NAME = 'version'

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == self.VARIABLE_NAME:
                self.version = node.value.s
        except:
            pass


def read_version():
    finder = VersionFinder()
    finder.visit(ast.parse(local_file('repocket', 'version.py')))
    return finder.version


requirements = [
    'redis==2.10.5',
    'python-dateutil==2.4.2',
]


setup(
    name='repocket',
    version='0.1.28',
    description='simple active record for redis',
    entry_points={
        'console_scripts': ['repocket = repocket.cli:main'],
    },
    author='Gabriel Falcao',
    author_email='gabriel@nacaolivre.org',
    url='http://repocket.readthedocs.org',
    packages=find_packages(exclude=['*tests*']),
    install_requires=requirements,
    zip_safe=False,
)
