# -*- coding: utf-8 -*-

# Created from https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='simdem',
    version='0.1.0',
    description='SimDem',
    long_description=readme,
    author='Tommy Falgout/Ross Gardler',
    author_email='thfalgou@microsoft.com',
    url='https://github.com/Azure/simdem',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'simdem=main:main'
        ]
    }
)

