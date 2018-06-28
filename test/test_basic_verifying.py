import logging

import requests
from mockserver import request, response, times
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestBasicVerifying(MockServerClientTestCase):
    def test_verify_request_received_once(self):
        result = requests.get(MOCK_SERVER_URL)
        logging.info("Elapsed {}".format(result.elapsed))
        self.client.verify(request(), times(1))

    def test_verify_request_never_received(self):
        self.client.verify(request(), times(0))

    def test_verify_request_not_received_fail(self):
        with self.assertRaises(AssertionError):
            self.client.verify(request(), times(1))

    def test_verify_all_expectations(self):
        self.client.expect(request(), response(), times(1))
        result = requests.get(MOCK_SERVER_URL)
        logging.info("Elapsed {}".format(result.elapsed))
        self.client.verify_expectations()
