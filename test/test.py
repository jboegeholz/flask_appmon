import json
import unittest
import datetime

from test_app import app_under_test
from appmon.app import create_app


class AppMonTest(unittest.TestCase):
    def setUp(self):
        # creates app under test
        self.app_under_test = app_under_test.test_client()
        self.app_under_test.testing = True

        # create app mon
        self.app_mon = create_app().test_client()
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

    # FIXME
    def get_aut_routes(self):
        # lets appmon call the list_routes endpoint from aut
        self.app_mon.post("register_app", data=dict(app_name='app_under_test', port='127.0.0.1:5000'))
        result = self.app_mon.get("/get_routes")
        self.assertEqual(result.status_code, 200)

    def test_receive_data(self):
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index', type="start", timestamp=datetime.datetime.now()))
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index', type="stop", timestamp=datetime.datetime.now()))
        result = self.app_mon.get("/get_hit_count?app=app_under_test&endpoint=/index")
        self.assertEqual(result.status_code, 200)
        assert json.loads(result.data)["hit_count"] == 1

    def test_receive_data_two_times(self):
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index2', type="start", timestamp=datetime.datetime.now()))
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index2', type="stop", timestamp=datetime.datetime.now()))
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index2', type="start", timestamp=datetime.datetime.now()))
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index2', type="stop", timestamp=datetime.datetime.now()))
        result = self.app_mon.get("/_get_hit_count?app=app_under_test&endpoint=/index2")
        self.assertEqual(result.status_code, 200)
        hit_count = json.loads(result.data)["hit_count"]
        assert hit_count == 2

    def test_hit_count(self):
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index2', type="start", timestamp=datetime.datetime.now()))
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index2', type="stop", timestamp=datetime.datetime.now()))
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index2', type="start", timestamp=datetime.datetime.now()))
        self.app_mon.post("receive_data", data=dict(app="app_under_test", endpoint='/index2', type="stop", timestamp=datetime.datetime.now()))
        result = self.app_mon.get("/hit_count")
        self.assertEqual(result.status_code, 200)



