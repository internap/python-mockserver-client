from typing import List

import requests
from mockserver_friendly import request, response, form, json_contains
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestRetrieveByMethod(MockServerClientTestCase):
    def test_retrieve_by_method(self):
        self.client.reset()
        requests.get(MOCK_SERVER_URL + "/whatever?foo=bar&hellow=world")
        requests.post(MOCK_SERVER_URL + "/whatever", json={"foo": "bar"})

        get_results: List[dict] = self.client.retrieve_recorded_requests(method='GET')

        assert len(get_results) == 1
        result = get_results[0]
        assert result.get('method') == 'GET'
        assert result.get('path') == '/whatever'
        assert result.get('queryStringParameters') == {'foo': ['bar'], 'hellow': ['world']}

    def test_retrieve_by_path(self):
        self.client.reset()
        requests.get(MOCK_SERVER_URL + "/whatever?foo=bar&hellow=world")
        requests.post(MOCK_SERVER_URL + "/whatever2", json={"foo": "bar"})

        get_results: List[dict] = self.client.retrieve_recorded_requests(path='/whatever')

        assert len(get_results) == 1
        result = get_results[0]
        assert result.get('method') == 'GET'
        assert result.get('path') == '/whatever'
        assert result.get('queryStringParameters') == {'foo': ['bar'], 'hellow': ['world']}

    def test_retrieve_by_querystring(self):
        self.client.reset()
        requests.get(MOCK_SERVER_URL + "/whatever?foo=bar&hellow=world")
        requests.post(MOCK_SERVER_URL + "/whatever2?foo=bar&hellow=world3", json={"foo": "bar"})

        get_results: List[dict] = self.client.retrieve_recorded_requests(querystring={"hellow": "world3"})

        assert len(get_results) == 1
        result = get_results[0]
        assert result.get('method') == 'POST'
        assert result.get('path') == '/whatever2'
        assert result.get('queryStringParameters') == {'foo': ['bar'], 'hellow': ['world3']}

    def test_retrieve_all(self):
        self.client.reset()
        requests.get(MOCK_SERVER_URL + "/whatever?foo=bar&hellow=world")
        requests.post(MOCK_SERVER_URL + "/whatever2?foo=bar&hellow=world3", json={"foo": "bar"})

        get_results: List[dict] = self.client.retrieve_recorded_requests()

        assert len(get_results) == 2

    def test_retrieve_body(self):
        self.client.reset()
        requests.get(MOCK_SERVER_URL + "/whatever?foo=bar&hellow=world")
        requests.post(MOCK_SERVER_URL + "/whatever2?foo=bar&hellow=world3", json={"foo": "bar"})

        get_results: List[dict] = self.client.retrieve_recorded_requests(method='POST')

        assert len(get_results) == 1
        result = get_results[0]
        assert result.get('method') == 'POST'
        assert result.get('path') == '/whatever2'
        assert result.get('queryStringParameters') == {'foo': ['bar'], 'hellow': ['world3']}
        assert result.get('body')["string"] == '{"foo": "bar"}'



