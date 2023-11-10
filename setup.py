"""
Generic setup for this python package
"""
from setuptools import find_packages, setup

setup(
    name="gitutils-cli",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "git_batch_merger=cli.git_batch_merger:git_batch_merger",
            "git_batch_cherry_picker=cli.git_batch_cherry_picker:git_batch_cherry_picker",
        ],
    },
)
