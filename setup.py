"""Setup script for DeFi Trading Bot."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="omega-defi-bot",
    version="1.0.0",
    author="FX Genius LLC",
    description="Multi-chain DeFi arbitrage trading bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "web3>=6.11.3",
        "aiohttp>=3.9.1",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
)
