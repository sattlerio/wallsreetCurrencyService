import app
import unittest
from config import TestingConfig
import json
from wallstreet.models import *
from flask_jwt_extended import decode_token


class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        app.app.config.from_object(TestingConfig)


    def test_ping_route(self):
        rv = self.app.get('/auth/ping')
        assert rv.status_code == 200
        assert b"pong" in rv.data

    def tearDown(self):
        app.db.session.remove()
        app.db.drop_all()
