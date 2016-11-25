import socket
import time
import threading


def tcpLink(sock, addr):
    print ('accept New connection from %s:%s..' % addr)
    sock.send(b'welcome')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        data = data.decode()
        if data == 'exit' or not data:
            break
        response = 'Hello %s' % data
        sock.send(response.encode('utf-8'))
    sock.close()


host = socket.gethostname()
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except OSError:
    s.close()
    s.bind((host,port))

s.listen(5)
while True:
    sock, add = s.accept()
    t = threading.Thread(target=tcpLink, args=(sock, add))
    t.start()
