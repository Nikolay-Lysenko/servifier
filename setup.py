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
    version='0.1.1',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nikolay-Lysenko/servifier',
    author='Nikolay Lysenko',
    author_email='nikolay-lysenco@yandex.ru',
    license='MIT',
    keywords='web_service api_maker apify ml_engineering model_to_production',
    packages=find_packages(exclude=['tests', 'docs']),
    python_requires='>=3.6',
    install_requires=['Flask']
)
