#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
from setuptools import setup, find_packages


def read_version():
    ctx = {}
    exec(local_file('httpretty', 'version.py'), ctx)
    return ctx['version']


local_file = lambda *f: \
    io.open(os.path.join(os.path.dirname(__file__), *f), encoding='utf-8').read()


requirements = [
    'redis==2.10.5',
    'python-dateutil==2.4.2',
]


setup(
    name='repocket',
    version='0.1.29',
    description='simple active record for redis',
    long_description=local_file('README.rst'),
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
