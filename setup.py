from setuptools import find_packages, setup

setup(
    name="zyte-tools",
    version="0.1",
    packages=find_packages(),
    scripts=["bin/stats_per_spider.py"],
)
