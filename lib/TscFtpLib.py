
# File: TscFtpLib.py ; This file is part of Twister.

# version: 2.002

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Wrapper other ftp library to create new API """

import ftplib

FTP = ftplib.FTP()

def ftp_open(host, port):
    """ open connection """
    f_open = FTP.connect(host, port)
    return f_open

def ftp_login(user, passwd):
    """ Login """
    f_login = FTP.login(user, passwd)
    return f_login

def ftp_dir():
    """ Show directory """
    f_dir = FTP.dir()
    return f_dir

def ftp_close():
    """ Close session """
    f_close = FTP.close()
    return f_close

def ftp_quit():
    """ Quit session """
    f_quit = FTP.quit()
    return f_quit

def ftp_delete(filename):
    """ Delete file """
    f_delete = FTP.delete(filename)
    return f_delete

def ftp_cwd(pathname):
    """ Get current directory """
    f_cwd = FTP.cwd(pathname)
    return f_cwd

def ftp_mkd(pathname):
    """ Make directory """
    f_mkd = FTP.mkd(pathname)
    return f_mkd

def ftp_pwd():
    """ Get remote directory """
    f_pwd = FTP.pwd()
    return f_pwd

def ftp_rmd(dirname):
    """ Remove remote directory """
    f_rmd = FTP.rmd(dirname)
    return f_rmd

def ftp_size(filename):
    """ Get size of file """
    f_size = FTP.size(filename)
    return f_size
