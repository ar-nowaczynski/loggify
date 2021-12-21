import pathlib
from setuptools import setup

README_PATH = pathlib.Path(__file__).parent / "README.md"
README_TEXT = README_PATH.read_text()

setup(
    name="loggify",
    version="0.2.1",
    license="MIT",
    description="Capture prints and tracebacks to a log file with 2 lines of code",
    long_description=README_TEXT,
    long_description_content_type="text/markdown",
    author="Arkadiusz Nowaczyński",
    author_email="ar.nowaczynski@gmail.com",
    url="https://github.com/ar-nowaczynski/loggify",
    packages=["loggify"],
    python_requires=">=3.7",
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
