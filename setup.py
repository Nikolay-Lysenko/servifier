"""
Just a regular `setup.py` file.

Author: Nikolay Lysenko
"""


import os
from setuptools import setup, find_packages


current_dir = os.path.abspath(os.path.dirname(__file__))

description = (
   'An easy-to-use tool for making web service with API '
   'from your own Python functions'
)
with open(os.path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='servifier',
    version='0.1.0',
    description=description,
    long_description=long_description,
    url='https://github.com/Nikolay-Lysenko/servifier',
    author='Nikolay Lysenko',
    author_email='nikolay-lysenco@yandex.ru',
    license='MIT',
    keywords='mle api web_service apify',
    packages=find_packages(exclude=['tests', 'docs']),
    python_requires='>=3.6',
    install_requires=['Flask']
)
