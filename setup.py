from setuptools import find_packages, setup

setup(
    name="zyte-utils",
    version="0.1",
    packages=find_packages(),
    scripts=[
        "bin/stats-per-spider",
        "bin/requests-per-spider",
    ],
)
