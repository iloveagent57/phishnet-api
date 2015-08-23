from setuptools import setup, find_packages
from codecs import open
from os import path


def read_requirements(req_file):
    with open(req_file) as f:
        return [line.strip() for line in f if line]


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='phishnet-api',
    version='1.0.0',
    description='A wrapper for the phish.net API',
    long_description=long_description,
    url='https://github.com/iloveagent57/phishnet-api',
    author='Alex Dusenbery',
    license='MIT',
    keywords='api wrapper phish',
    packages=find_packages(exclude=['tests*']),
    install_requires=read_requirements(path.join(here, 'requirements.txt')),
)