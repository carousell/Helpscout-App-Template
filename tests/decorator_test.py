from unittest import TestCase
from mock import patch, Mock
from helpscout_app.decorators import signed_request


class DecoratorTest(TestCase):
    def test_signed_request(self):
        # Patch Flask's request, current_app and the is_helpscout_request helper function
        request_patcher = patch('helpscout_app.decorators.request',
                                headers={'X-Helpscout-Signature': '123'})
        MockRequest = request_patcher.start()
        app_patcher = patch('helpscout_app.decorators.current_app', config={})
        MockApp = app_patcher.start()
        helpscout_patcher = patch('helpscout_app.decorators.is_helpscout_request')
        MockHelpScout = helpscout_patcher.start()

        # If helper function returns False, decorator should not call the callable
        MockHelpScout.return_value = False
        decorated_func = signed_request(lambda x: x)
        self.assertEquals(('', 400), decorated_func(1))

        # Else, continue with the callable
        MockHelpScout.return_value = True
        decorated_func = signed_request(lambda x: x)
        self.assertEquals(1, decorated_func(1))
