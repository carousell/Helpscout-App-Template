import hmac
import hashlib
import base64
from unittest import TestCase
from helpscout_django.helpscout import is_helpscout_request


class HelpScoutTest(TestCase):
    def test_is_helpscout_request(self):
        secret = 'abc'
        request_data = '{"test": "data"}'
        dig = hmac.new(secret, msg=request_data, digestmod=hashlib.sha1).digest()
        helpscout_sig = base64.b64encode(dig).decode()

        self.assertFalse(is_helpscout_request(secret, request_data, 'aloha'))
        self.assertTrue(is_helpscout_request(secret, request_data, helpscout_sig))
