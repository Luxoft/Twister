
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
