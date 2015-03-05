
# version: 2.000

import os
import re
import json
import subprocess
import base64
from BasePlugin import BasePlugin
from common import helpers

#

class Plugin(BasePlugin):
    """
    Packet sniffer plugin
    """
    def __init__(self,user,data):
        BasePlugin.__init__(self,user,data)
        self.cap_dir = helpers.userHome(user) + '/twister/pcap'
        print 'CAP_DIR: {}'.format(self.cap_dir)


    def run(self, args):
        """
        Supported commands: 'tshark_getpackets',
                            'tshark_getfilelist',
                            'tshark_delete_files',
                            'tshark_delete_all_files',
                            'tshark_download_file'
        """
        if not os.path.isdir(self.cap_dir):
            return False
        command = args['command'][0]
        if command == 'tshark_getpackets':
            cap_file = args['cap_file'][0]
            print cap_file
            ret_str=self.get_packets(cap_file)
            return ret_str  
        elif command == 'tshark_getfilelist':
            ret_str=self.get_file_list()
            return ret_str
        elif (command == 'tshark_delete_files'):
            file_list = args['cap_file'][0]
            ret_str=self.remove_file_list(command, file_list)
            return ret_str
        elif (command == 'tshark_delete_all_files'):
            ret_str=self.remove_file_list(command)
            return ret_str
        elif (command == 'tshark_download_file'):
            cap_file = args['cap_file'][0]
            ret_str = self.download_file(cap_file)
            return ret_str
        else:
            print 'Command unknown {}'.format(command)
            return False
        return True


    def get_packets(self, cap_file):
        """
        returns packets from a captured file
        """
        #read tshark flags from the cfg file.
        tshark_flags = ''
        tshark_params=['tshark', '-r', self.cap_dir + '/' + cap_file]
        tshark_params = tshark_params + [tshark_flags]
        #summary
        p=subprocess.Popen(tshark_params, stdout=subprocess.PIPE)
        out, err = p.communicate()
        summary=out.splitlines()
        #details
        tshark_params.append('-V')
        p=subprocess.Popen(tshark_params, stdout=subprocess.PIPE)
        out, err = p.communicate()
        lines=out.splitlines()
        ftime=True
        dstr=""
        details=[]
        for l in lines:
            res=re.match("Frame \d+:",l)
            l+="\n"
            if res != None:
                if ftime == True:
                    ftime = False
                else:
                    details.append(dstr)
                    dstr=""
            dstr+=l
        details.append(dstr)
        tdict={'tshark_getpackets':{'tshark_packets_summary':summary, 'tshark_packets_detail':details}}
 
        ret_str=json.dumps(tdict, sort_keys=True, indent=4, separators=(',', ': '))
        return ret_str


    def get_file_list(self):
        """
        returns a list of files with the captured packets
        """
        mtime = lambda f: os.stat(os.path.join(self.cap_dir, f)).st_mtime
        flist = list(sorted(filter(lambda f: f.split('.')[1] == 'cap', os.listdir(self.cap_dir)), key=mtime))
        #create response
        tdict = {'tshark_getfilelist':flist}
        ret_str = json.dumps(tdict, sort_keys=True, indent=4, separators=(',', ': '))
        return ret_str


    def remove_file_list(self, command,files=''):
        """
        `tshark_delete_files`: deletes a list of files selected by the user
        `tshark_delete_all_files`: deletes all files in folder
        """
        if command == 'tshark_delete_files':
            lst=files.split(',')
            for f in lst:
                capname = self.cap_dir+'/'+f.strip()
                #cfgname = '{}/{}{}'.format(self.cap_dir, f.strip().split('.')[0], '.cfg')
                if os.path.isfile(capname):
                    # and os.path.isfile(cfgname):
                    try:
                        os.remove(capname)
                        # os.remove(cfgname)
                    except Exception as e:
                        print 'File {} cannot be removed: {}'.format(capname, e)
                        return False

        elif command == 'tshark_delete_all_files':
            for f in os.listdir(self.cap_dir):
                fname=self.cap_dir+'/'+f
                if os.path.isfile(fname):
                    try:
                        os.remove(fname)
                    except Exception as e:
                        print 'File {} cannot be removed: {}'.format(fname, e)
                        return False
        return True


    def download_file(self, cap_file):
        """
        moves the file in to user's specified path
        """
        fdonwload = self.cap_dir + '/' + cap_file
        if os.path.isfile(fdonwload):
            with open(fdonwload, 'rb') as f:
                data = f.read()
                b_64 = base64.b64encode(data)
                return b_64
        else:
            print 'File {} not found.'.format(fdonwload)
        return ''

#
