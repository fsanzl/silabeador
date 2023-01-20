import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work #
setup(
    name="silabeador",
    version="1.1.11-2",
    python_requires='>=3.5',
    description="A Python library of methods and functions for syllabic division and prosodic stress detecting for Spanish",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/fsanzl/silabeador",
    project_urls={
        'Source': 'https://github.com/fsanzl/silabeador/',
        'Tracker': 'https://github.com/fsanzl/silabeador/issues',
    },
    author="Fernando Sanz-Lázaro",
    author_email="fsanzl@gmail.com",
    license="LGPL",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Natural Language :: Spanish",
    ],
    packages=["silabeador"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "silabeador=silabeador.__main__:main",
        ]},
    package_data={'silabeador': ['*.lst']},
)
