import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    install_require = f.read().splitlines()

setuptools.setup(
    name="sparclclient",
    version="0.0.3",
    url="https://github.com/noaodatalab/sparclclient",
    python_requires=">=3.6",
    description="A client for getting spectra data from NOIRLab.",

    author="NOIRLab DataLab",
    author_email="datalab@noirlab.edu",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=install_require,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
)
