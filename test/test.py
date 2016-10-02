import unittest

from test.test_app import app_under_test


class FlaskBookshelfTests(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app_under_test = app_under_test.test_client()
        # propagate the exceptions to the test client
        self.app_under_test.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app_under_test.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app_under_test.get('/')

        # assert the response data
        self.assertEqual(result.data, "Hello World")
