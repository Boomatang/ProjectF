import flask
import unittest
from cgi.main_app import app


class FlaskrTestCase(unittest.TestCase):
    def setup(self):
        app.config['TESTING'] = True
        self.app = app.test_client(self)

    def teardown(self):
        print('teardown')

    def test_index(self):
        self.app = app.test_client(self)
        rv = self.app.get('/', content_type='html/text')
        self.assertTrue(b'Hello World' in rv.data)

    def test_page_path_index(self):
        self.app = app.test_client(self)
        rv = self.app.get('/', content_type='html/text')
        self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
    unittest.main()