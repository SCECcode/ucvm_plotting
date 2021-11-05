[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![GitHub repo size](https://img.shields.io/github/repo-size/sceccode/ucvm_plotting)
[![ucvm_plotting-ci Actions Status](https://github.com/SCECcode/ucvm_plotting/workflows/ucvm_plotting-ci/badge.svg)](https://github.com/SCECcode/ucvm_plotting/actions)

# ucvm_plotting

<a href="http://www.scec.org/research"><img src="https://github.com/sceccode/ucvm_plotting/wiki/blob/main/images/ucvm_plotting_logo.png"></a>

# Description: 
This ucvm_plotting software was originally included in UCVM v19.4.0 which was released in June 2019. In 2021, the plotting utilities in UCVM v19.4 were moved into this standalone repository. 

The UCVM plotting utilities make use of Python2 libraries which will must be converted to Python3 for continued development. The current plotting utilities rely on Python2, which must be installed on systems using these utilities.

UCVM_plotting is distributed as open-source scientific software. It can be installed compiled and run on most Linux-based computer systems if the system includes software development tools including Python, C, and Fortran compilers, and other software tools. The UCVM v19.4.0 source code is distributed using a github repository. On Github, users can find the source code, installation directions for Linux, and a wiki that provide examples and the expected results from UCVM.

# Table of Contents:
1. [Software Documentation](https://github.com/SCECcode/ucvm_plotting/wiki/blob/main/images/ucvm_plotting_logo.png)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Support](#support)
5. [Contributing](#contributing)
6. [Credits](#credits)
7. [License](#license)

# Installation: 
Prerequisite :  anaconda2/python2/matplotlib/basemap

* install UCVM per instruction, https://github.com/SCECcode/ucvm/wiki
* source ucvm's install_loc/conf/ucvm_env.sh
* git clone https://github.com/SCECcode/ucvm_plotting.git
* cd into ucvm_plotting
* ./unpack-dist

# Usage:
Once both ucvm and ucvm_plotting are installed, users can run ucvm_plotting scripts like this:
<pre>
./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 0.0 -d poisson -a s -c cs173h -o cs173h_poisson_map.png
</pre>
[<img src="https://github.com/SCECcode/ucvm_plotting.wiki/blob/main/images/plots/make_plots/cs173h_poisson_map.png" width="300" height="300" />](http://github.com/SCECcode/ucvm_plotting.wiki/blob/main/images/plots/make_plots/cs173h_poisson_map.png)


# Support:
Support for UCVM is provided by that Southern California Earthquake Center (SCEC) Research Computing Group. This group supports several research software distributions including UCVM. Users can report issues and feature requests using UCVM's github-based issue tracking link below. Developers will also respond to emails sent to the SCEC software contact listed below.
1. [UCVM Github Issue Tracker:](https://github.com/SCECcode/ucvm_plotting/issues)
2. Email Contact: software@scec.usc.edu

# Contributing:
We welcome contributions to the UCVM_plotting software utilities. An overview of the process for contributing seismic models or 
software updates to the UCVM_plotting Project is provided in the UCVM_plotting [contribution guidelines](CONTRIBUTING.md). 
UCVM_plotting contributors agree to abide by the code of conduct found in our [Code of Conduct](CODE_OF_CONDUCT.md) guidelines.

# Credits:
Development of UCVM_plotting is a group effort. A list of developers that have contributed to the UCVM Software framework 
are listed in the [Credits.md](CREDITS.md) file in this repository.

# License:
The UCVM software is distributed under the BSD 3-Clause open-source license. 
Please see the [LICENSE.txt](LICENSE.txt) file for more information.
