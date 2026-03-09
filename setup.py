"""Laciyo package configuration."""

from setuptools import setup, find_packages

setup(
    name="laciyo",
    version="0.1.0",
    description="Laciyo – Latin Cyber Creole conlang toolkit",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "laciyo=laciyo.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
