import os
import sys
import unittest
import json

from tornado.testing import AsyncHTTPTestCase
from tornado.options import define, options
import app


class TestApp(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_list(self):
        response = self.fetch('/list')
        self.assertEqual(response.code, 200)
        js = json.loads(response.body)
        self.assertTrue('data' in js)
        self.assertTrue(len(js['data']) > 0)

    def test_list_args(self):
        response = self.fetch('/list?date_min=2019.01.16T00:00:00')
        self.assertEqual(response.code, 200)
        js = json.loads(response.body)
        self.assertTrue('data' in js)
        self.assertTrue(len(js['data']) > 0)

    def test_count(self):
        response = self.fetch('/count?group=os')
        self.assertEqual(response.code, 200)
        js = json.loads(response.body)
        self.assertTrue('data' in js)
        self.assertTrue(len(js['data']) > 0)

    def test_count_failure(self):
        response = self.fetch('/count?group=123')
        self.assertEqual(response.code, 400)
 
if __name__ == '__main__':
    tornado.options.parse_command_line()
    unittest.main()
