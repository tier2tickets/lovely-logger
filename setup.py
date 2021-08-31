import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lovely_logger",
    version="1.0.6",
    description="A logger library which builds on, combines, and simplifies various logging features of Python 3",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tier2tickets/lovely_logger",
    author="Chris Wheeler",
    author_email="grintor@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["lovely_logger"],
    include_package_data=False,
    install_requires=[],
)