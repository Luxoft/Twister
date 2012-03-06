
import telnetlib


tn = telnetlib.Telnet()

def telnet_open(host, port):
    telnet_open = tn.open(host, port)

def telnet_send(msg):
    telnet_send = tn.write(msg)

def telnet_expect(msg):
    telnet_expect = tn.expect(msg)

def telnet_close():
    telnet_close = tn.close()
