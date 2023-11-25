"""
Generic setup for this python package
"""
from setuptools import find_packages, setup

setup(
    name="gitutils-cli",
    version="0.5.00",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gitutils-merge=cli.git_batch_merger:git_batch_merger",
            "gitutils-cherry-pick=cli.git_batch_cherry_picker:git_batch_cherry_picker",
        ],
    },
)
