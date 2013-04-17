
import socket, ssl, pprint,time

#wrap ssl socket with ca_certs
def ssl_socket_ca(s):
    ssl_sock = ssl.wrap_socket(s,
                               ssl_version=ssl.PROTOCOL_TLSv1,
                               ca_certs="cacert.pem",
                               cert_reqs=ssl.CERT_REQUIRED)                           
    return ssl_sock
    
#wrap ssl socket without ca_certs                               
def ssl_socket(s):
    ssl_sock = ssl.wrap_socket(s,ssl_version=ssl.PROTOCOL_TLSv1)                           
    return ssl_sock                               
    

def test_ssl_connection(ca_certs=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(ca_certs==True):
        print "*** test ssl with ca_certs ***"    
        ssl_sock=ssl_socket_ca(s)
    else:
        print "\n*** test ssl without ca_certs ***"    
        ssl_sock=ssl_socket(s)
        
    ssl_sock.connect(('127.0.0.1', 8080))
    print repr(ssl_sock.getpeername())
    print ssl_sock.cipher()
    print pprint.pformat(ssl_sock.getpeercert())
    for i in range(0,10):
        ssl_sock.send("Echo "+str(i))
        data=ssl_sock.recv()
        print data
        time.sleep(1)
    ssl_sock.close()

def main():
    test_ssl_connection(ca_certs=True)
    test_ssl_connection(ca_certs=False)        

if __name__ == '__main__':
    main()                    
# note that closing the SSLSocket will also close the underlying socket


