#!/usr/bin/python
import ipaddress
import socket

import service
import pytest


@pytest.mark.unit
def test_get_ip_address_returns_unknown_ip():
    # Arrange
    def receive_hostname(hostname):
        raise socket.gaierror

    # Act
    result = service._get_ip_address("TEST_HOSTNAME", receive_hostname)

    # Assert
    assert result == 'UNKNOWN_IP'


@pytest.mark.integration
def test_get_ip_address():
    # Act
    result = service._get_ip_address(socket.gethostname(), socket.gethostbyname)

    # Assert
    try:
        ipaddress.ip_address(result)
    except:
        assert False, "Invalid IP address"
