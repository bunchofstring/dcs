#!/usr/bin/python
import socket
import sys

_port = int(sys.argv[1])

_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_socket.bind(('', _port))
_socket.listen(1)

_hostname = socket.gethostname()
_ip_address = socket.gethostbyname(_hostname)

while True:
  (_connection, _address) = _socket.accept()
  print('Connection from {}'.format(_address))

  _request = _connection.recv(1024).decode()
  print('Received request: {}'.format(_request))

  _response = 'HTTP/1.0 200 OK\n\nHello from {} ({})'.format(_hostname,_ip_address)
  _connection.sendall(_response.encode())
  _connection.close()

_socket.close()