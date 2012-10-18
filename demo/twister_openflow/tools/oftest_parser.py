
import os
import re
import sys
import inspect
sys.path.append("../oflib/")
sys.path.append("../")

import of_config
import basic
from basic import *
import caps
from caps import *
import pktact
from pktact import *
import errormsg
from errormsg import *

def get_class_body(classname):
    print classname
    class_body=""
    classobj=eval(classname)
    lines = inspect.getsourcelines(classobj)
    for line in lines[0]:
        class_body+=line
    return class_body

def parse_test_suite(config):
    tc_list=[]
    tc_template=config['tc_template']
    tc_list_name=config['tc_list_name']
    tc_ignore_list=config['tc_ignore_list']
    tc_path=config['tc_path']
    tc_suite=config['tc_suite']

    with open(tc_suite, 'r') as f:
        print "Reading test suite: %s\n" % tc_suite
        data=f.read()
        m=re.findall('class\s+\w+\(.*?\):\s*\"{3}[\S\s]*?\"{3}',data)
        if(m):
            for text in m:
                classdesc=""
                classname=re.match('class(\s+\w+)\(.*?\):',text)
                classdesc=re.search('\"{3}([\S\s]*?)\"{3}',text)
                if(classname):
                    tc_class=classname.group(1).strip()
                    tc_list.append(tc_class)
                    suite_name = os.path.split(tc_suite)[-1].split('.')[0]
                    tc_file=tc_path+"%s%s.py" % (suite_name,tc_class)
                    if not tc_class in tc_ignore_list:
                        class_body=get_class_body(tc_class)
                        with open(tc_file, 'w') as f1:
                            tc_content=tc_template % (class_body,tc_class)
                            f1.write(tc_content)
