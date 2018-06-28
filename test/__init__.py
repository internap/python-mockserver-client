import logging
import time
import unittest

from mockserver import MockServerClient

MOCK_SERVER_URL = "http://localhost:1080"


class Timed(object):
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        logging.info('{} START'.format(self.msg))
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        logging.info(self.msg + ' took %0.3f ms' % (self.interval*1000.0))


class SlowMockServerClient(MockServerClient):
    def _call(self, command, data=None):
        #time.sleep(0.01)
        with Timed("Calling {}".format(command)):
            result = super(SlowMockServerClient, self)._call(command, data)
            logging.info("call elapsed from request {}".format(result.elapsed))
            return result


class MockServerClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = SlowMockServerClient(MOCK_SERVER_URL)

    def tearDown(self):
        self.client.reset()
