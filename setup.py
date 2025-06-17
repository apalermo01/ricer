from setuptools import find_packages, setup

setup(
    name="ricer",
    version="0.1",
    install_requires=[
        "pydantic",
        "pyyaml",
        "jinja2",
        "matplotlib",
        "pytest",
        "numpy",
        "toml",
    ],
    packages=find_packages(),
)
