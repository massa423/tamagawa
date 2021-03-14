from telnetlib import Telnet

import pytest


class TamagawaClient:
    def __init__(self):
        self.host = "localhost"
        self.port = 3333
        self.timeout = 10

    def open(self):
        self.client = Telnet(self.host, self.port, self.timeout)

    def send(self, data: bytes):
        self.client.write(data)
        response = self.client.read_all()
        self.client.close()

        return response

    def close(self):
        self.client.close()


@pytest.fixture
def tamagawa():
    t = TamagawaClient()
    t.open()
    yield t
    t.close()
