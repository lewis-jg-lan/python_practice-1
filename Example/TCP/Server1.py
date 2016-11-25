import socket

host = socket.gethostname()
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)
sock, addr = s.accept()
print('Linked')
info = sock.recv(1024)
info = info.decode()
while info != 'exit':
    print('From other :%s' % info)
    send_mes = raw_input('')
    sock.send(send_mes.encode('utf-8'))
    if send_mes == 'exit':
        break
    info = sock.recv(1024)
socket.close()
s.close()
