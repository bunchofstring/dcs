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
    service.handle_requests(my_socket)


if __name__ == '__main__':
    main(sys.argv[1:])
