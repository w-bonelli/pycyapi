#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='plantit',
    version='0.3.31',
    description='phenotyping container workflows on laptops, clusters, or the cloud',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Computational Plant Science Lab',
    author_email='wbonelli@uga.edu',
    license='BSD-3-Clause',
    url='https://github.com/Computational-Plant-Science/plantit-cli',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'plantit = plantit_cli.cli:cli'
        ]
    },
    python_requires='>=3.6.8',
    install_requires=['requests', 'pyaml', 'click', 'tenacity', 'tqdm', 'python-irodsclient'],
    setup_requires=['setuptools', 'wheel'],
    tests_require=['pytest', 'coveralls'])
