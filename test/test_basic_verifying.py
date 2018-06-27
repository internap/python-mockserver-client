import requests
from mockserver import request, response, times
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestBasicVerifying(MockServerClientTestCase):
    def test_verify_request_received_once(self):
        requests.get(MOCK_SERVER_URL)
        self.client.verify(request(), times(1))
