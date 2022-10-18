#!/usr/bin/python
import socket
import time

import sandbox
import pytest
import service
import threading

sandbox_warmup_duration = 5
any_port = [0]
request_count = 1000
max_duration = 1


@pytest.mark.system
def test_main(mocker):
    # Arrange
    spy = mocker.spy(service, 'listen_to')

    # Act
    _start_sandbox(any_port)

    # Assert
    hostinfo = spy.spy_return.getsockname()
    response = _fetch_response(hostinfo, "TEST_ANY_REQUEST")
    assert "Hello from" in response, "Received incorrect response {}".format(response)


@pytest.mark.system
def test_main_performance(mocker):
    # Arrange
    spy = mocker.spy(service, 'listen_to')
    _start_sandbox(any_port)
    hostinfo = spy.spy_return.getsockname()
    response_list = []

    # Act
    start_timestamp = time.monotonic()
    for _ in range(request_count):
        response = _fetch_response(hostinfo, "TEST_PERFORMANCE_ANY_REQUEST")
        response_list.append(response)
    elapsed = time.monotonic() - start_timestamp
    print("Executed {} request/response iterations in {} seconds".format(request_count, elapsed))

    # Assert
    response_count = len(response_list)
    assert elapsed < max_duration, "Test execution took {} seconds (max is {} seconds)" \
        .format(elapsed, max_duration)
    assert response_count == request_count, "Expected {} responses, but only received {}"\
        .format(request_count, response_count)


def _fetch_response(hostinfo, message):
    with _new_socket_connection(hostinfo) as s:
        s.sendall(message.encode())
        return s.recv(2048).decode()


def _new_socket_connection(hostinfo):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(hostinfo)
    return s


def _start_sandbox(port):
    background_thread = threading.Thread(target=sandbox.main, args=[port])
    background_thread.daemon = True
    background_thread.start()
    time.sleep(sandbox_warmup_duration)
