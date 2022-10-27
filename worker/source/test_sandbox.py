#!/usr/bin/python
import socket
import time

import sandbox
import pytest
import service
import threading

sandbox_warmup_duration = 5
any_port = [0]
request_count = 2000
max_duration = 1
performance_timeout = max_duration + sandbox_warmup_duration


@pytest.mark.system
def test_main_response(mocker):
    # Arrange
    spy = mocker.spy(service, 'listen_to')

    # Act
    _start_sandbox(any_port)

    # Assert
    hostinfo = spy.spy_return.getsockname()
    response = _fetch_response(hostinfo, "TEST_ANY_REQUEST")
    assert "Hello from" in response, "Received incorrect response {}".format(response)


class TestPerformance:

    response_list = []
    hostinfo = None

    @pytest.fixture(autouse=True)
    def sandbox_lifecycle(self, mocker):
        # Arrange
        self.response_list.clear()
        spy = mocker.spy(service, 'listen_to')
        _start_sandbox(any_port)
        self.hostinfo = spy.spy_return.getsockname()

    @pytest.mark.system
    @pytest.mark.timeout(performance_timeout)
    def test_performance_main_success_rate(self):
        # Act
        elapsed = _request_repeatedly_timed(self.hostinfo, self.response_list.append)

        # Assert
        assert elapsed < max_duration, "Test execution took {} seconds (max is {} seconds)" \
            .format(elapsed, max_duration)

    @pytest.mark.system
    @pytest.mark.timeout(performance_timeout)
    def test_performance_main_throughput(self):
        # Act
        _request_repeatedly_timed(self.hostinfo, self.response_list.append)

        # Assert
        response_count = len(self.response_list)
        assert response_count == request_count, "Expected {} responses, but only received {}" \
            .format(request_count, response_count)


def _request_repeatedly_timed(hostinfo, on_response):
    start_timestamp = time.monotonic()
    for _ in range(request_count):
        response = _fetch_response(hostinfo, "TEST_PERFORMANCE_ANY_REQUEST")
        on_response(response)
    elapsed = time.monotonic() - start_timestamp

    print("Transactions per second = {} (i.e. {} request/response iterations in {} seconds)"
          .format(request_count / elapsed, request_count, elapsed))

    return elapsed


def _fetch_response(hostinfo, message):
    with _new_socket_connection(hostinfo) as s:
        s.sendall(message.encode())
        return s.recv(2048).decode()


def _new_socket_connection(hostinfo):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(hostinfo)
    return s


def _start_sandbox(port):
    threading.Thread(
        target=sandbox.main,
        args=[port],
        daemon=True
    ).start()
    time.sleep(sandbox_warmup_duration)
