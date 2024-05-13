from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "This module enables users to upload data to DaRUS the dataverse of the university of Stuttgart"

# Setting up
setup(
    name="FAIRDaRUS",
    version=VERSION,
    description=DESCRIPTION,
    url="https://github.com/FAIRChemistry/FAIRDaRUS.git",
    author="Samir Darouich",
    author_email="samir.darouich@itt.uni-stuttgart.de",
    license_files=("LICENSE"),
    packages=find_packages(),
    install_requires=["sdrdm", "easyDataverse", "ipywidgets"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Users",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
