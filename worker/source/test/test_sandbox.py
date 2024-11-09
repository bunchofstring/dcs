#!/usr/bin/python
import socket
import threading
import time

import pytest

import worker.sandbox as sandbox
import worker.service as service

ANY_PORT = [0]


@pytest.mark.unit
def test_main_service_integration(mocker):
    # Arrange
    mocks = {
        'listen_to': mocker.DEFAULT,
        'handle_requests': mocker.DEFAULT
    }
    service_mock = mocker.patch.multiple('worker.service', **mocks)

    # Act
    _start_sandbox(ANY_PORT, 0)

    # Assert
    for mocked_method in mocks:
        service_mock[mocked_method].assert_called_once()


class TestPerformance:
    SANDBOX_WARMUP_DURATION = 1 / 1000
    MAX_PERFORMANCE_TEST_DURATION = 2
    PERFORMANCE_TEST_TIMEOUT_THRESHOLD = SANDBOX_WARMUP_DURATION + MAX_PERFORMANCE_TEST_DURATION
    PERFORMANCE_REQUEST_COUNT = 5000

    hostinfo = None
    response_list = None

    @pytest.fixture(scope="class", autouse=True)
    def sandbox_lifecycle_warmstart(self, class_mocker):
        # Arrange
        spy = class_mocker.spy(service, 'listen_to')
        _start_sandbox(ANY_PORT, self.SANDBOX_WARMUP_DURATION)
        hostinfo = spy.spy_return.getsockname()
        self.__class__.hostinfo = hostinfo
        self.__class__.response_list = []
        _fetch_response(hostinfo, "TEST_ANY_REQUEST")

    @pytest.mark.system
    def test_main_response(self):
        # Act
        response = _fetch_response(self.hostinfo, "TEST_ANY_REQUEST")

        # Assert
        assert "Hello from" in response, "Received incorrect response {}".format(response)

    @pytest.mark.system
    @pytest.mark.timeout(PERFORMANCE_TEST_TIMEOUT_THRESHOLD)
    def test_performance_main_throughput(self):
        # Act
        start_timestamp = time.monotonic()
        _request_repeatedly(self.hostinfo, self.PERFORMANCE_REQUEST_COUNT)
        elapsed = time.monotonic() - start_timestamp
        print("Transactions per second = {} (i.e. {} request/response iterations in {} seconds)"
              .format(self.PERFORMANCE_REQUEST_COUNT / elapsed, self.PERFORMANCE_REQUEST_COUNT, elapsed))

        # Assert
        assert elapsed < self.MAX_PERFORMANCE_TEST_DURATION, "Execution took {} seconds (max is {} seconds)" \
            .format(elapsed, self.MAX_PERFORMANCE_TEST_DURATION)

    @pytest.mark.system
    @pytest.mark.timeout(PERFORMANCE_TEST_TIMEOUT_THRESHOLD)
    def test_performance_main_success_rate(self):
        # Act
        _request_repeatedly(self.hostinfo, self.PERFORMANCE_REQUEST_COUNT, self.response_list.append)

        # Assert
        response_count = len(self.response_list)
        assert response_count == self.PERFORMANCE_REQUEST_COUNT, "Expected {} responses, but received {}" \
            .format(self.PERFORMANCE_REQUEST_COUNT, response_count)


def _request_repeatedly(hostinfo, request_count, on_response=lambda noop: None):
    for _ in range(request_count):
        response = _fetch_response(hostinfo, "TEST_PERFORMANCE_ANY_REQUEST")
        on_response(response)


def _fetch_response(hostinfo, message):
    with _new_socket_connection(hostinfo) as s:
        s.sendall(message.encode())
        return s.recv(2048).decode()


def _new_socket_connection(hostinfo):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(hostinfo)
    return s


def _start_sandbox(port, startup_time):
    threading.Thread(
        target=sandbox.main,
        args=[port],
        daemon=True
    ).start()
    time.sleep(startup_time)
