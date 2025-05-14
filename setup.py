from setuptools import setup
from setuptools import find_packages

setup(
    name="imup-cli",
    description="Upload Files, to your Univerity Server",
    long_description="Yeah... description is already good enough",
    version="0.1.0",
    url="https://github.com/minmagdec/imup",
    author="Levi Drieling",
    scripts=["scripts/imup"],
    packages=find_packages("src"),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[]
)
