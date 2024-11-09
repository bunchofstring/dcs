#!/usr/bin/python

# Could be achieved via mocker, but this class is test-framework-agnostic
class MockSocketObject:
    # Not strictly necessary, but improves performance
    @staticmethod
    def bind(_):
        pass

    @staticmethod
    def listen(_):
        pass
