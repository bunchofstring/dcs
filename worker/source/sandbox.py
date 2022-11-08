#!/usr/bin/python
import sys

import service

# listen on all interfaces
host = ''


def main(args):
    if len(args) != 1:
        raise TypeError("Incorrect number of arguments. Please provide a port number")

    port = int(args[0])

    my_socket = service.listen_to(host, port)
    response = service.prepare_response()

    try:
        while True:
            (connection, address) = my_socket.accept()
            service.process_request(connection, address)
            connection.sendall(response)
            connection.close()
    finally:
        my_socket.close()


if __name__ == '__main__':
    main(sys.argv[1:])
