#!/usr/bin/python
import socket
import threading


def listen_to(host, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((host, port))
    my_socket.listen(1)
    return my_socket


def handle_requests(my_socket):
    try:
        while True:
            (connection, address) = my_socket.accept()
            response = _process_request(connection, address)
            connection.sendall(response)
            connection.close()
    finally:
        my_socket.close()


def _process_request(connection_dependency, address):
    request = connection_dependency.recv(1024).decode()
    print('Connection from {} - received {}'.format(address, request))
    return _prepare_response()


def _prepare_response():
    hostinfo = _get_host_info(socket)
    response = 'HTTP/1.0 200 OK\n\nHello from {} ({})'.format(*hostinfo)
    return response.encode()


def _get_ip_address(hostname, get_host_by_name_dependency):
    try:
        return get_host_by_name_dependency(hostname)
    except socket.gaierror as e:
        print("Could not get IP address for {}:\n{}".format(hostname, e))
        return 'UNKNOWN_IP'


def _get_host_info(socket_dependency):
    hostname = socket_dependency.gethostname()
    ipaddress = _get_ip_address(hostname, socket_dependency.gethostbyname)
    return hostname, ipaddress
