#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# flake8: noqa
from __future__ import absolute_import
from __future__ import print_function

import io
from os import path

from setuptools import setup
from setuptools import find_packages


here = path.abspath(path.dirname(__file__))


def read(*names, **kwargs):
    return io.open(path.join(here, *names), encoding=kwargs.get("encoding", "utf8")).read()

about = {}
exec(read("src", "compas_cadwork", "__version__.py"), about)

long_description = read("README.md")
requirements = read("requirements.txt").split("\n")
optional_requirements = {}

setup(
    name=about["__title__"],
    version=about["__version__"],
    license=about["__license__"],
    description=about["__description__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license="MIT license",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords=[],
    project_urls={},
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={},
    data_files=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    python_requires=">=3.8",
    extras_require=optional_requirements,
    entry_points={
        "console_scripts": [],
    },
    ext_modules=[],
)
