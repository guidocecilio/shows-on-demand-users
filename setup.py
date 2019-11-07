"""
Standard setup.py for easy install

For development do
# python setup.py develop
"""
from setuptools import setup, find_packages

packages = find_packages('src')
version = "0.1"

setup(
    name="users",
    version=version,
    zip_safe=False,
    packages=packages,
    package_dir={'': 'src'},
    include_package_data=True,
)
