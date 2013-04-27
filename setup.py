from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    with open('microirc/version.txt') as f:
        return f.read().strip()


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''

setup(
    name='microirc',
    version=get_version(),
    description='Micro IRC is an IRC toolkit to develop IRC client or bot, especially for Python/IRC beginner.',
    long_description=get_readme(),
    author='Jeong YunWon',
    author_email='jeong+microirc@youknowone.org',
    url='https://github.com/youknowone/microirc',
    packages=(
        'microirc',
    ),
    package_data={
        'microirc': ['version.txt']
    },
    install_requires=[
        'distribute',
    ],
)