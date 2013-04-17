import ssl
from gevent.server import StreamServer


def echo(socket, address):
    print ('New connection from %s:%s' % address)    
    while True:
        data = socket.recv(2048)
        if not data:
            print ("client disconnected")
            break
        print "Receiving: "+ data
        data="Server echo reply: " + data
        socket.send(data)
        
def main():    
    host="0.0.0.0"
    port=8080
    print "Starting ssl stream server:",host+":"+str(port)
    server = StreamServer((host,port), 
                      echo, 
                      keyfile="ctl-privkey.pem", 
                      certfile="ctl-cert.pem",    
                      ca_certs="cacert.pem",
                      ssl_version=ssl.PROTOCOL_TLSv1
                      )
    server.serve_forever()
    
if __name__ == '__main__':
    main()                
