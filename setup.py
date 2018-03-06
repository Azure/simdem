# -*- coding: utf-8 -*-
""" Setup.py """

# Created from https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='simdem',
    version='0.9.0',
    description='SimDem',
    long_description=README,
    author='Tommy Falgout, Ross Gardler',
    author_email='thfalgou@microsoft.com',
    url='https://github.com/Azure/simdem',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'simdem=simdem.cli:main'
        ]
    }
)
