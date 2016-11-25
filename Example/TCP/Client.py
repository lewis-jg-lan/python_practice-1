import  socket

host = socket.gethostname()
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

print(s.recv(1024))
for data in ['Allen','Tracy','Sarah']:
    s.send(data.encode('utf-8'))
    print(s.recv(1024))

s.send(b'exit')
s.close()
