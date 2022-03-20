import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pdfmb",
    version="0.0.4",
    description="Merge PDFs with bookmarks",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/1081/pdfmb",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(include=["pdfmb"]),
    include_package_data=True,
    install_requires=["pikepdf"],
)

# Upload to pypi
# 1. python setup.py sdist bdist_wheel
# 2. twine upload dist/*
