# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='fracfocustools',
    version='0.0.5',
    description='Tools for maipulating data acquired from fracfous.org',
    long_description=readme,
    author='Paul Woods, SkyTruth',
    author_email='paul@skytruth.org',
    url='https://github.com/SkyTruth/fracfocustools',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=["pdfminer"],
    package_data = {'': ['README.md', 'LICENSE']},
    include_package_data = True
)
