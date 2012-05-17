
# File: TscFtp.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristian Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>

# Twister is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.

# Twister is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Twister.  If not, see <http://www.gnu.org/licenses/>.

import ftplib

ftp = ftplib.FTP()

def ftp_open(host, port):
    ftp_open = ftp.connect(host, port)

def ftp_login(user, passwd):
    ftp_login = ftp.login(user, passwd)

def ftp_dir():
    ftp_dir = ftp.dir()

def ftp_close():
    ftp_close = ftp.close()

def ftp_quit():
    ftp_quit = ftp.quit()

def ftp_delete(filename):
    ftp_delete = ftp.delete(filename)

def ftp_cwd(pathname):
    ftp_cwd = ftp.cwd(pathname)

def ftp_mkd(pathname):
    ftp_mkd = ftp.mkd(pathname)

def ftp_pwd():
    ftp_pwd = ftp.pwd()

def ftp_rmd(dirname):
    ftp_rmd = ftp.rmd(dirname)

def ftp_size(filename):
    ftp_size = ftp.size(filename)
