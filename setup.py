"""
  @file setup.py
  @brief Build and install the pycvm
  @author The SCEC/UCVM Developers - <software@scec.usc.edu>

"""

from setuptools import setup


NAME = "ucvm_plotting"
FULLNAME = "ucvm_plotting with pycvm"
AUTHOR = "The SCEC/UCVM Developers"
AUTHOR_EMAIL = "software@scec.usc.edu"
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = "Apache 2.0 license"
URL = "https://github.com/SCEC/ucvm_plotting"
DESCRIPTION = "Python code extensions for UCVM and plotting library for the SCEC UCVM"

with open("README.md") as f:
    LONG_DESCRIPTION = "".join(f.readlines())

VERSION = "0.0.1"

CLASSIFIERS = [
    "Development Status :: 1 - Alpha",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 2.7",
    "License :: OSI Approved :: {}".format(LICENSE),
]
PLATFORMS = "Any"
INSTALL_REQUIRES = ["numpy", "matplotlib", "basemap", "basemap-data-hires", "packaging"]
KEYWORDS = ["UCVM"]

if __name__ == "__main__":
    setup(
        name=NAME,
        fullname=FULLNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        url=URL,
        platforms=PLATFORMS,
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        install_requires=INSTALL_REQUIRES,
        packages=["pycvm"], 
#        package_data = {"pygmt.tests": ["data/*", "baseline/*"]},
#        scripts=['ucvm_plotting/*','utilities/*','scripts/*','examples/*'] 
    )
