#!/usr/bin/python
import ipaddress
import platform
import socket

import pytest

import service

unsupported_platform = {
    'condition': platform.system() != 'Linux',
    'reason': "Test only produces meaningful results in a production-like Linux environment"
}


@pytest.mark.skipif(**unsupported_platform)
@pytest.mark.system
def test_get_valid_ip_address():
    # Act
    result = service._get_ip_address(socket.gethostname(), socket.gethostbyname)

    # Assert
    try:
        ipaddress.ip_address(result)
    except ValueError:
        assert False, "Invalid IP address: {}".format(result)


@pytest.mark.integration
def test_get_ip_address_returns_unknown_ip():
    # Arrange
    def receive_hostname(*_, **__):
        raise socket.gaierror

    # Act
    result = service._get_ip_address("TEST_HOSTNAME", receive_hostname)

    # Assert
    assert result == 'UNKNOWN_IP'


@pytest.mark.integration
def test_listen_to_port(mocker):
    # Arrange
    socket_object_mock = MockSocketObject()
    socket_method_mock = mocker.patch('socket.socket', return_value=socket_object_mock)
    bind_method_mock = mocker.patch.object(socket_object_mock, 'bind', return_value=None)
    listen_method_mock = mocker.patch.object(socket_object_mock, 'listen', return_value=None)

    # Act
    service.listen_to("localhost", 0)

    # Assert
    socket_method_mock.assert_called_once()
    bind_method_mock.assert_called_once()
    listen_method_mock.assert_called_once()


@pytest.mark.unit
def test_listen_to_port_returns_object(mocker):
    # Arrange
    socket_method_mock = mocker.patch('socket.socket')
    socket_object_mock = MockSocketObject()
    mocker.patch.object(socket_object_mock, 'bind', return_value=None)
    mocker.patch.object(socket_object_mock, 'listen', return_value=None)
    socket_method_mock.return_value = socket_object_mock

    # Act
    result_socket = service.listen_to("localhost", 0)

    # Assert
    assert result_socket is not None, "Did not return the resulting socket"


@pytest.mark.unit
def test_prepared_response_includes_required_info(mocker):
    # Arrange
    required_info = ('TEST_IP_ADDRESS', 'TEST_HOST_NAME')
    mocker.patch('service._get_host_info', return_value=required_info)

    # Act
    response = service.prepare_response()

    # Assert
    contains_required_info = all(x.encode() in response for x in required_info)
    assert contains_required_info, "Could not find both '{}' and '{}' in the response '{}'"\
        .format(*required_info, response)


@pytest.mark.unit
def test_get_hostinfo_returns_tuple():
    # Act
    hostinfo = service._get_host_info(MockSocketPackage())

    # Assert
    assert len(hostinfo) == 2, "Expected a tuple with two elements in return"


class MockSocketPackage:
    # Not strictly necessary, but certainly improves speed and isolation
    # from the host system state (which is irrelevant to this test)
    @staticmethod
    def gethostname():
        return 'TEST_HOST_NAME'

    @staticmethod
    def gethostbyname(_):
        return 'TEST_IP_ADDRESS'


class MockSocketObject:
    # Not strictly necessary, but certainly improves speed and isolation
    # from the host system state (which is irrelevant to this test)
    @staticmethod
    def bind(_):
        pass

    @staticmethod
    def listen(_):
        pass
