import setuptools

from pkgutil import walk_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gornilo", # Replace with your own username
    version="0.0.4",
    author="rx00",
    author_email="rx00@hackerdom.com",
    description="AD CTFs checker wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rx00/Gornilo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)