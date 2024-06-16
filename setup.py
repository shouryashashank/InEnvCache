from setuptools import find_packages, setup
import pathlib
with open("README.md", "r") as f:
    long_description = f.read()

HERE = pathlib.Path(__file__).parent

setup(
    name="inenvcache",
    version="0.0.100",
    description="A caching framework to cache object across pods within an environment  ",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shouryashashank/InEnvCache",
    author="shouryashashank",
    author_email="shouryashashank@gmail.com",
    license="AGPLv3+",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",   
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],  
    install_requires=["bson >= 0.5.10",
                      "pycryptodome >= 3.20.0"],

    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
