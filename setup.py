#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pyFirmata>=1.1.0', 'transitions==0.8.8']

test_requirements = ['pytest>=3', ]

setup(
    author="Drew Meyers",
    author_email='drewm@mit.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Software for controlling the Open Flow-through sampling device.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='open_flow_through',
    name='open_flow_through',
    packages=find_packages(include=['open_flow_through', 'open_flow_through.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/drewmee/open_flow_through',
    version='0.1.0',
    zip_safe=False,
)
