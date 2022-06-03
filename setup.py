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

VERSION = "0.0.3"

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
INSTALL_REQUIRES = ["numpy", "matplotlib", "basemap", "packaging"]
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
        scripts=["ucvm_plotting/make_map_grid.py","ucvm_plotting/plot_compare_plot.py",
"ucvm_plotting/plot_cross_section.py","ucvm_plotting/plot_density_plot.py",
"ucvm_plotting/plot_depth_profile.py","ucvm_plotting/plot_elevation_cross_section.py",
"ucvm_plotting/plot_elevation_horizontal_slice.py","ucvm_plotting/plot_elevation_map.py",
"ucvm_plotting/plot_elevation_profile.py","ucvm_plotting/plot_horizontal_slice.py",
"ucvm_plotting/plot_scatter_plot.py","ucvm_plotting/plot_vs30_etree_map.py",
"ucvm_plotting/plot_vs30_map.py","ucvm_plotting/plot_z10_map.py",
"ucvm_plotting/plot_z25_map.py",
"utilities/makegrid.sh","utilities/view_png.py"] 
    )
