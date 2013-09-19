
# File: ExecutionManager.py ; This file is part of Twister.

# version: 2.001

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
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

import os
import sys

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('$TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)


from common.constants  import *
from common.helpers    import *

#

class ExecutionManager(object):
    """
    Execution Manager class organizes the EP / Suite / Testcase functions.
    """

    def __init__(self, proj):
        self.project = proj


    def resetProject(self, user):
        " "
        twister_cache = userHome(user) + '/twister/.twister_cache'
        setFileOwner(user, twister_cache)
        return self.project.reset(user)


    def getUserVariable(self, user, variable):
        " "
        data = self.project.getUserInfo(user, variable)
        if data is None: data = False
        return data


    def setUserVariable(self, user, key, variable):
        " "
        return self.project.setUserInfo(user, key, variable)


    def listEPs(self, user):
        " "
        epList = self.project.getUserInfo(user, 'eps').keys()
        return ','.join(epList)


    def getEpVariable(self, user, epname, variable, compress=False):
        " "
        return self.project.getEpInfo(user, epname).get(variable, False)


    def setEpVariable(self, user, epname, variable, value):
        " "
        return self.project.setEpInfo(user, epname, variable, value)


    def listSuites(self, user, epname):
        " "
        suiteList   = [str(k)+':'+v['name'] for k, v in self.project.getEpInfo(user, epname)['suites'].items()]
        return ','.join(suiteList)


    def getSuiteVariable(self, user, epname, suite, variable):
        " "
        data = self.project.getSuiteInfo(user, epname, suite)
        if not data: return False
        return data.get(variable, False)


    def getFileVariable(self, user, epname, file_id, variable):
        " "
        data = self.project.getFileInfo(user, epname, file_id)
        if not data: return False
        return data.get(variable, False)


    def setFileVariable(self, user, epname, filename, variable, value):
        " "
        return self.project.setFileInfo(user, epname, filename, variable, value)


    def getGlobalVariable(self, user, var_path):
        " "
        return self.project.getGlobalVariable(user, var_path, False)


    def setGlobalVariable(self, user, var_path, value):
        " "
        return self.project.setGlobalVariable(user, var_path, value)


    def getConfig(self, user, cfg_path, var_path):
        " "
        return self.project.getGlobalVariable(user, var_path, cfg_path)


# # #


    def registerClient(self, user, clients):
        " "
        return False


    def startEP(self, user, epname):
        " "
        return False


    def stopEP(self, user, epname):
        " "
        return False


    def restartEP(self, user, epname):
        " "
        return False


# # #


    def getEpStatus(self, user, epname):
        " "
        return False


    def getEpStatusAll(self, user):
        " "
        return False


    def setEpStatus(self, user, epname, new_status, msg=''):
        " "
        return self.project.setExecStatus(user, epname, new_status, msg)


    def setEpStatusAll(self, user, new_status, msg=''):
        " "
        return self.project.setExecStatusAll(user, new_status, msg)


# # #


    def getLibrariesList(self, user='', all=True):
        " "
        return False


    def downloadLibrary(self, user, name):
        " "
        return False


    def getTestFile(self, user, epname, file_id):
        " "
        return False


    def getEpFiles(self, user, epname):
        " "
        return False


    def getSuiteFiles(self, user, epname, suite):
        " "
        return False


# Eof()
