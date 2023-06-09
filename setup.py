# see https://packaging.python.org/tutorials/packaging-projects/#configuring-metadata
# python3 -m build --wheel; twine upload dist/*

import setuptools
import sys

sys.path.append(".")
from sparcl import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements-client.txt") as f:
    install_require = f.read().splitlines()

setuptools.setup(
    name="sparclclient",
    # version="0.3.19",
    version=__version__,  # see sparcl/__init__.py
    author="NOIRLab DataLab",
    author_email="datalab-spectro@noirlab.edu",
    description="A client for getting spectra data from NOIRLab.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astro-datalab/sparclclient",
    project_urls={
        "Documentation": "https://sparclclient.readthedocs.io/en/latest/",
    },
    #! project_urls={
    #!     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    #! },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    #! package_dir={"": "src"},
    packages=setuptools.find_packages(),
    install_requires=install_require,
    python_requires=">=3.6",
)
