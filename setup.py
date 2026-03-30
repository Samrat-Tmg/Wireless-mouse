#!/usr/bin/env python
"""Setup script for Touchpad."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="touchpad-mouse",
    version="1.0.0",
    author="Touchpad Contributors",
    author_email="dev@example.com",
    description="Wireless mouse control via Bluetooth - turn your mobile device into a touchpad",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/touchpad",
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "touchpad-server=server.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
