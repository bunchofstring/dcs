#!/usr/bin/python

# Could be achieved via mocker, but this class is test-framework-agnostic
class MockSocketObject:
    # Not strictly necessary, but certainly improves speed and isolation
    # from the host system state (which is irrelevant to this test)
    @staticmethod
    def bind(_):
        pass

    @staticmethod
    def listen(_):
        pass
