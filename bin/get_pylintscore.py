#!/usr/local/bin/python2.7
#----------------------------------------------------------------------------------------------------------
#File Name:     get_pylintscore.py
#Author:        smisra
#
#Purpose:       To recursively check the pylint scores for twister client and server
#
#Execution:     Can be run from twister
#----------------------------------------------------------------------------------------------------------

import os
import re
#import sys
from subprocess import Popen, PIPE

folder_list = ["~/twister/client", "~/twister/bin", "~/twister/common", "/opt/twister/server", "/opt/twister/bin", "/opt/twister/lib", "/opt/twister/services"]
scorelevel = "file" #other option is folder
counter = 0
files = []
filelist = []
results = {}

for folder in folder_list:
    print "Checking pylint scores for ", folder
    if scorelevel == "folder":
        print os.system("pylint " + folder)
    else:
        files.append(os.popen("find " + folder + " -type f -name '*.py'").read())
for flname in files:
    if flname != '':
        filelist.append(flname.split('\n'))
print filelist

for section in filelist:
    for file in section:
        if file != '':
            counter += 1
            print "Checking pylint score for file: ", file
            print os.system("pylint "+ file)
print "Totally processed ", counter," files"

'''
for section in filelist:
    for file in section:
        if file != '':
            pylint = Popen(("pylint -f text %s" % file).split(), stdout=PIPE)
            pylint.wait()
            output = pylint.stdout.read()
            print output

            #results_re = re.compile(r"Your code has been rated at ([\d\.]+)/10  /(previous run: [\d\.]+/10, +0.00/)")
            results_re = re.compile(r"Your code has been rated at ([\d\.]+)")
            print results_re
            results[file] = results_re.findall(output)
            print "Here's the result: ", results[file]
print results.items()
'''
_RESULT = 'pass'
