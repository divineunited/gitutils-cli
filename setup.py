"""
Generic setup for this python package
"""
from setuptools import find_packages, setup

setup(
    name="gitutils-cli",
    version="0.2",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gitbatch_merge=cli.git_batch_merger:git_batch_merger",
            "gitbatch_cherry-pick=cli.git_batch_cherry_picker:git_batch_cherry_picker",
        ],
    },
)
