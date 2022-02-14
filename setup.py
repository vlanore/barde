from pathlib import Path

from setuptools import setup  # type: ignore

setup(
    name="barde",
    version="0.1",
    description=Path("README.md").read_text(),
    author="vlanore",
    author_email="vincent.lanore@gmail.com",
    packages=["barde"],
    install_requires=["brython"],
)
