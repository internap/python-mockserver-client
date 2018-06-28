import logging

import requests
from mockserver import request, response, times, json_equals, json_contains
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestJsonExpectations(MockServerClientTestCase):

    def test_expect_json_equals(self):
        self.client.expect(
            request(body=json_equals({"key": "value", "key1": "value2"})),
            response(),
            times(1)
        )

        result = requests.get(MOCK_SERVER_URL + "/path", json={"key": "value"})
        logging.info("Elapsed {}".format(result.elapsed))
        self.assertEquals(result.status_code, 404)

        result = requests.get(MOCK_SERVER_URL + "/path", json={"key": "value", "key1": "value2"})
        logging.info("Elapsed {}".format(result.elapsed))
        self.assertEquals(result.status_code, 200)

    def test_expect_json_contains(self):
        self.client.expect(
            request(body=json_contains(
                {"key": "value"}
            )),
            response(),
            times(1)
        )

        result = requests.get(MOCK_SERVER_URL + "/path", json={"key1": "value2"})
        logging.info("Elapsed {}".format(result.elapsed))
        self.assertEquals(result.status_code, 404)

        result = requests.get(MOCK_SERVER_URL + "/path", json={"key1": "value2", "key": "value"})
        logging.info("Elapsed {}".format(result.elapsed))
        self.assertEquals(result.status_code, 200)
