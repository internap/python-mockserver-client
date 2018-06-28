import time
import unittest

from mockserver import MockServerClient

MOCK_SERVER_URL = "http://localhost:1080"


class SlowMockServerClient(MockServerClient):
    def _call(self, command, data=None):
        time.sleep(0.01)
        return super()._call(command, data)


class MockServerClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = MockServerClient(MOCK_SERVER_URL)

    def tearDown(self):
        self.client.reset()
