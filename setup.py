#!/usr/bin/env python

from setuptools import setup

setup(
    name="kropotkin",
    version="0.0.0",
    author="Ross Fenning",
    author_email="github@rossfenning.co.uk",
    packages=["kropotkin"],
    description="Hooks for stateless Django apps",
    install_requires=["msgpack", "hhc"],
)
