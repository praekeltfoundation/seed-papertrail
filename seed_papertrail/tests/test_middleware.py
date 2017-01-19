import django
from django.conf import settings
from django.test.client import RequestFactory
from seed_papertrail.middleware import (
    request_timing_middleware, RequestTimingMiddleware)

from unittest import TestCase
from testfixtures import log_capture

settings.configure(USE_TZ=True)
django.setup()


class TestMiddleware(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def noop(self, arg=None):
        return arg

    @log_capture()
    def test_middleware(self, l):
        middleware = request_timing_middleware('papertrail', level='DEBUG')
        request = self.factory.get('/')
        response = middleware(self.noop)(request)
        self.assertEqual(request, response)
        self.assertTrue(str(l).startswith('papertrail DEBUG'))

    @log_capture()
    def test_middleware_old_django(self, l):
        middleware = RequestTimingMiddleware()
        request = self.factory.get('/')
        middleware.process_request(request)
        middleware.process_response(request, None)
        self.assertTrue(str(l).startswith('papertrail INFO'))
