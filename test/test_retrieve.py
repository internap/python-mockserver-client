import requests
from retry.api import retry_call
from mockserver import request, response
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestRetrieve(MockServerClientTestCase):
    def test_retrieve_expectations(self):
        self.client.stub(
            request(),
            response()
        )
        requests.get(MOCK_SERVER_URL)
        assert retry_call(self.client.retrieve,
                          fkwargs=({"type": "RECORDED_EXPECTATIONS"}),
                          tries=10, delay=0.3)

    def test_retrieve_expectations_with_request(self):
        path = "/test_path"
        self.client.stub(request(path=path), response())
        requests.get(MOCK_SERVER_URL + path)
        assert retry_call(self.client.retrieve,
                          fkwargs=({"type": "RECORDED_EXPECTATIONS", "request": request(path=path)}),
                          tries=10, delay=0.3)

    def test_retrieve_requests(self):
        requests.get(MOCK_SERVER_URL)
        assert retry_call(self.client.retrieve, fargs=("REQUESTS",), tries=10, delay=0.3)

    def test_retrieve_requests_with_request(self):
        requests.get(MOCK_SERVER_URL + '/path')
        assert retry_call(self.client.retrieve,
                          fkwargs=({"type": "REQUESTS", "request": request(path='/path')}),
                          tries=10, delay=0.3)
