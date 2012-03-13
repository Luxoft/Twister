
'''
Twister has the following dependencies:

- Python 2.7     : The Central Engine, the Execution Process, the Test Runner, the Resource Allocator
                 : and the reporting framework are all written in Python.

- BeautifulSoup  : www.crummy.com/software/BeautifulSoup/
                 : Parses XML and HTML documents easily
                 : (BeautifulSoup is included in `trd_party` folder and should not be installed)

- MySQL-python   : mysql-python.sourceforge.net/
                 : Connects to MySQL databases
                 : (MySQL-python requires the python2.7-dev headers in order to compile)

- CherryPy       : www.cherrypy.org/
                 : High performance, minimalist Python web framework
                 : (CherryPy is used to serve the reports and the Java Applet)

- Mako           : www.makotemplates.org/
                 : Hyperfast and lightweight templating for the Python platform
                 : (Mako is used for the reports)

- Beaker         : beaker.readthedocs.org/
                 : Library for caching and sessions, in web applications and stand-alone Python scripts
                 : (Beaker is optional; it is used by Mako, to cache the pages for better performance)

- pExpect        : sourceforge.net/projects/pexpect/
                 : Spawn child applications, control them, respond to expected patterns in their output
                 : (pExpect is optional; it is used by the Python test cases, to connect to FTP/ Telnet)

'''

import os, sys
import tarfile

fopen = tarfile.open("twister.tar.gz")
root_folder = fopen.getnames()[0]
#fopen.extractall()
fopen.close()
