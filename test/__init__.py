import unittest

from mockserver import MockServerClient

MOCK_SERVER_URL = "http://localhost:1080"


class MockServerClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = MockServerClient(MOCK_SERVER_URL)

    def tearDown(self):
        self.client.reset()
