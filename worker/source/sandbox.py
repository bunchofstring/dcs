#!/usr/bin/python
import service
import sys


def main(args):
    port = int(args[0])
    my_socket = service.listen_to(port)
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
