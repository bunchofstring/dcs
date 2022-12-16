#!/usr/bin/python

# Could be achieved via mocker, but this class is test-framework-agnostic

# Not strictly necessary, but certainly improves speed and isolation
# from the host system state (which is irrelevant to this test).
@staticmethod
def gethostname():
    return 'TEST_HOST_NAME'

@staticmethod
def gethostbyname(_):
    return 'TEST_IP_ADDRESS'
