import unittest

from test_app import app_under_test
from appmon.appmon import app_mon


class AppMonTest(unittest.TestCase):
    def setUp(self):
        # creates app under test
        self.app_under_test = app_under_test.test_client()
        self.app_under_test.testing = True

        # create app mon
        self.app_mon = app_mon.test_client()
        self.app_mon.testing = True

    def tearDown(self):
        pass

    def test_list_routes(self):
        # an app under test must implement an endpoint which returns all routes
        result = self.app_under_test.get('/list_routes')
        self.assertEqual(result.status_code, 200)

    def test_register_app(self):
        result = self.app_mon.post("register_app", data=dict(app_name='app_under_test', port='127.0.0.1:5000'))
        self.assertEqual(result.status_code, 200)

    def test_get_aut_routes(self):
        # lets appmon call the list_routes endpoint from aut
        self.app_mon.post("register_app", data=dict(app_name='app_under_test', port='127.0.0.1:5000'))
        result = self.app_mon.get("get_routes")
        self.assertEqual(result.status_code, 200)


