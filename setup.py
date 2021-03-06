#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().split('\n')

with open('requirements-dev.txt') as req_file:
    requirements_dev = req_file.read().split('\n')

with open('VERSION') as fp:
    version = fp.read().strip()

setup(
    name='seed-papertrail',
    version=version,
    description="This is the seed-papertrail project.",
    long_description=readme,
    author="Praekelt.org",
    author_email='dev@praekelt.org',
    url='https://github.com/praekeltfoundation/seed-papertrail',
    packages=[
        'seed_papertrail',
    ],
    package_dir={'seed_papertrail':
                 'seed_papertrail'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='seed papertrail',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ]
)
