from setuptools import find_packages, setup

setup(
    name="wexample-config",
    version=open("version.txt").read(),
    author="weeger",
    author_email="contact@wexample.com",
    description="Helpers to manage dict types configurations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wexample/python-config",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "wexample-helpers",
    ],
    python_requires=">=3.6",
)
