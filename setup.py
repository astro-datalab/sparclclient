# see https://packaging.python.org/tutorials/packaging-projects/#configuring-metadata

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    install_require = f.read().splitlines()

setuptools.setup(
    name="sparclclient",
    version="0.0.7",
    author="NOIRLab DataLab",
    author_email="datalab@noirlab.edu",
    description="A client for getting spectra data from NOIRLab.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noaodatalab/sparclclient",
    #! project_urls={
    #!     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    #! },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    #! package_dir={"": "src"},
    packages=setuptools.find_packages(),
    install_requires=install_require,
    python_requires=">=3.6",

)
