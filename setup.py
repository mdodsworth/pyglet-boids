# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='boids',
    version='0.0.1',
    description='Boids simulation project',
    long_description=readme,
    author='Michael Dodsworth',
    author_email='michael@dodsy.me',
    url='https://github.com/mdodsworth/pyglet-boids',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'gui_scripts': [
            'boids = boids.__main__:main'
            ]
        },
)

