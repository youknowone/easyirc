from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    with open('easyirc/version.txt') as f:
        return f.read().strip()


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''

setup(
    name='easyirc',
    version=get_version(),
    description='Easy IRC is an IRC toolkit to develop IRC client or bot, especially for Python/IRC beginner.',
    long_description=get_readme(),
    author='Jeong YunWon',
    author_email='jeong+easyirc@youknowone.org',
    url='https://github.com/youknowone/easyirc',
    packages=(
        'easyirc',
        'easyirc/command',
        'easyirc/event',
        'easyirc/client',
    ),
    package_data={
        'easyirc': ['version.txt']
    },
    install_requires=[
        'distribute',
        'prettyexc',
        'cacheobj==0.8.2',
    ],
)
