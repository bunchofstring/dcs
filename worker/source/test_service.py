#!/usr/bin/python
import ipaddress
import socket

import service
import pytest


@pytest.mark.system
def test_listen_to_port():
    # Act
    result_socket = service.listen_to("localhost", 0)

    # Assert
    os_assigned_port = result_socket.getsockname()[1]
    assert os_assigned_port > 0, "Invalid port assignment"


@pytest.mark.system
def test_get_ip_address():
    # Act
    result = service._get_ip_address(socket.gethostname(), socket.gethostbyname)

    # Assert
    try:
        ipaddress.ip_address(result)
    except ValueError:
        assert False, "Invalid IP address"


@pytest.mark.integration
def test_get_ip_address_returns_unknown_ip():
    # Arrange
    def receive_hostname(_hostname):
        raise socket.gaierror

    # Act
    result = service._get_ip_address("TEST_HOSTNAME", receive_hostname)

    # Assert
    assert result == 'UNKNOWN_IP'


@pytest.mark.unit
def test_get_hostinfo_returns_tuple(mocker):
    # Arrange
    mocker.patch('service._get_ip_address', return_value='TEST_IP_ADDRESS')
    mocker.patch('socket.gethostname', return_value='TEST_HOST_NAME')

    # Act
    hostinfo = service._get_host_info(socket)

    # Assert
    assert len(hostinfo) == 2, "Expected a tuple with two elements in return"


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
