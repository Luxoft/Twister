
import time
import datetime
import os
import sys
import json
import stat
import thread
import threading
import select

try:
    from scapy.all import *
except Exception as e:
    print 'Install scapy python module {}'.format(e)
    sys.exit(1)


class TSharkHandler(object):

    def __init__(self, active, interface, read_flags, write_flags, max_packets, cap_file, cap_dir):
        """
        Initialize the sniffer handler.
        """
        self.active = active
        self.interface = interface
        self.cap_file = cap_file
        self.cap_dir = cap_dir
        self.max_packets = max_packets

        #TShark read flags
        self.read_flags=[]
        rflags = read_flags.split(' ')
        self.read_flags = self.read_flags+rflags 

        #TShark write flags
        self.write_flags = ['-i', self.interface]
        wflags = write_flags.split(' ')
        self.write_flags = self.write_flags + wflags

        self.handler = TSharkEmu(self.max_packets, iface=self.interface, filter=write_flags)


    def createCapFile(self):
        """
        Creates the file where the packets will be stored.
        """
        with open(self.cap_file, 'w') as f:
            f.close()


    def start(self):
        """
        Starts the capture.
        """
        if(self.active == True):
            self.createCapFile()
            self.handler.startCapture(self.cap_file, self.write_flags)
            return True
        else:
            print 'tShark not enabled.'
            return False


    def stop(self):
        """
        Stops the capture.
        """
        self.handler.stopCapture()
        self.active=False
        return True


class TSharkEmu(threading.Thread):
    def __init__(self, max_packets, *arg,**karg):
        """
        A separate thread that actually captures the packets.
        """
        threading.Thread.__init__(self)
        self.arg = arg
        self.karg = karg
        self.packets = []
        self.cap_file = None
        self.active = False
        self.lock = thread.allocate_lock()
        self.lock.acquire()
        self.max_packets = max_packets
        self.packet_count = 0


    def stopCapture(self):
        """
        The is stopped and the packets are written into a file
        """
        if(len(self.packets) > 0):
            wrpcap(self.cap_file, self.packets)
        else:
            print 'No packets were captured!'
        self.packets = []
        self.packet_count = 0
        if(not self.lock.locked()):
            self.lock.acquire()

    def startCapture(self, cap_file, tshark_flags):
        """
        The capture is initiated. A the capturing thread is started.
        """
        self.cap_file = cap_file
        if(self.active == False):
            self.start()
            self.active = True 
        else:
            print 'The sniffer is already running.'
        if(self.lock.locked()):
            self.lock.release()
        
    def run(self):
        """
        Here the packets are captured.
        The scapy library is used.
        """
        L2socket = conf.L2listen
        #print 'args: {}'.format(self.arg)
        #print 'kargs: {}'.format(self.karg)
        s = L2socket(type=ETH_P_ALL, *self.arg, **self.karg)
        while True:
            sel = select.select([s],[],[],None)
            if s in sel[0]:
                p = s.recv(MTU)
                if p is None:
                    break
                self.packet_count += 1
                if(self.packet_count > self.max_packets):
                    print 'Maximum packets captured.'
                    time.sleep(0.5)
                    continue
                self.packets.append(p)
                with self.lock:
                    pass



SNIFFER_HANDLER = None

def start_capture(tshark_enabled, 
                  tshark_iface = 'lo', 
                  tshark_read_flags= '', 
                  tshark_write_flags = '',
                  max_packets = 1000,
                  tshark_cap_dir = os.getenv('TWISTER_PATH')):
    """
    Is the interface for the user to start a packet capture.

    tshark_iface = the interface that tShark is listening to
    tshark_read_flags= '-R of13.ofp_header'
    tshark_write_flags = 'port 6633' -> acts like a filter.
    """
    global SNIFFER_HANDLER

    # verify that the client/EP runs with root privileges
    if os.getuid() != 0:
        print 'The client should run with root privileges'
        return False
    # tshark should be installed to be able to capture packets
    try:
        os.system('tshark -v')
    except Exception as e:
        print 'Please install tshark before starting the packet capture {}'.format(e)
        return False

    cap_file = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')+'.cap'
    print 'CAP_FILE: {}'.format(cap_file)
    print tshark_cap_dir
    if 'pcap' not in os.listdir(tshark_cap_dir):
        tshark_cap_dir += '/'+'pcap'
        try:
            os.mkdir(tshark_cap_dir)
            os.chmod(tshark_cap_dir, stat.S_IRWXG|stat.S_IRWXU|stat.S_IRWXO)
        except Exception as e:
            print 'Cannot make `{}` directory {}'.format(tshark_cap_dir, e)
            return False
    else:
        tshark_cap_dir += '/pcap'
    cap_file = tshark_cap_dir+'/'+cap_file
    if SNIFFER_HANDLER is None:
        SNIFFER_HANDLER = TSharkHandler(tshark_enabled,
                                        tshark_iface,
                                        tshark_read_flags,
                                        tshark_write_flags,
                                        max_packets,
                                        cap_file, 
                                        tshark_cap_dir)
        SNIFFER_HANDLER.start()
        print 'Sniffer started ...'
    else:
        print 'Another capture is running. Please stop the current capture before starting another one!'
        return False
    return True


def stop_capture():
    """
    Is the interface for the user to stop the current capture.
    """
    global SNIFFER_HANDLER
    if not SNIFFER_HANDLER:
        print 'The capture was not started!'
        return False
    SNIFFER_HANDLER.stop()
    print 'Sniffer stopped ...'
#     config_file = SNIFFER_HANDLER.cap_file[:-3]+'cfg'
#     config = open(config_file, 'w')
#     sniffer_config = {'interface' : SNIFFER_HANDLER.interface,
#                 'max_packets' : SNIFFER_HANDLER.max_packets,
#                 'read_flags' : SNIFFER_HANDLER.read_flags,
#                 'write_flags' : SNIFFER_HANDLER.write_flags}
#     print 'SNIFFER_CONFIG: {}'.format(sniffer_config)
#     json.dump(sniffer_config, config)
#     config.close()
    SNIFFER_HANDLER = None
    return True