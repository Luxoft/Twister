
# File: TscFtp.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

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
