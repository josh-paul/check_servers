#!/usr/bin/env python

from setuptools import setup, find_packages

desc = ''
with open('README.rst') as f:
    desc = f.read()

setup(
    name='check_servers',
    version='0.0.1',
    description=('Utility to collect json data from status endpoint on many servers.'),
    long_description=desc,
    url='https://github.com/josh-paul/check_servers',
    author='Josh Paul',
    author_email='trevalen@me.com',
    license='Apache v2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='server servers status check server_status_check',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    install_requires=['requests', 'tabulate'],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={'console_scripts': ['check_servers=servers.status:cli']},
)
