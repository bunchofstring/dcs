#!/usr/bin/python
import socket


def listen_to(host, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((host, port))
    my_socket.listen(1)
    return my_socket


def prepare_response():
    hostinfo = _get_host_info(socket)
    response = 'HTTP/1.0 200 OK\n\nHello from {} ({})'.format(*hostinfo)
    return response.encode()


def process_request(connection_dependency, address):
    request = connection_dependency.recv(1024).decode()
    print('Connection from {} - received {}'.format(address, request))


def _get_ip_address(hostname, get_host_by_name_dependency):
    try:
        return get_host_by_name_dependency(hostname)
    except socket.gaierror as e:
        print("Error getting IP address for {}:\n{}".format(hostname, e))
        return 'UNKNOWN_IP'


def _get_host_info(socket_dependency):
    hostname = socket_dependency.gethostname()
    ipaddress = _get_ip_address(hostname, socket_dependency.gethostbyname)
    return hostname, ipaddress
