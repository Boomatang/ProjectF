import re
import unittest

from cgi.database import Database
from cgi.main_app import app
from cgi.sql_scripts import clean_master


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client(self)
        self.fay = Database('test_login_master_files')

    def tearDown(self):
        self.fay.execute(clean_master)
        self.fay.conn_close()


    # Tests on the public home page goes here
    def test_index(self):
        rv = self.app.get('/', content_type='html/text')
        self.assertTrue(b'This is the main home page for the public' in rv.data)


    def test_page_path_index(self):
        rv = self.app.get('/', content_type='html/text')
        self.assertEqual(rv.status_code, 200)


    # test all urls inside the body tags
    def test_public_index_urls_check(self):
        urls = self.app.get('/', content_type='html/text')
        urls = str(urls.data)
        body_data = re.search('(<body>.*?</body>)', urls, re.DOTALL)
        urls = re.findall('href="(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"', str(body_data))

        for url in urls:
            path = url.split('"')
            rv = self.app.get(path[1], content_type='html/text', follow_redirects=True)
            self.assertEqual(rv.status_code, 200, msg=path)


    # test for the sign up page
    def test_sign_up_content(self):
        rv = self.app.get('/signup/', content_type='html/text')
        massage = rv.data
        self.assertTrue(b'This is the first page of the sign up forms' in rv.data, msg=massage)


    def test_page_path_sign_up(self):
        rv = self.app.get('/signup/', content_type='html/text')
        massage = rv.data
        self.assertEqual(rv.status_code, 200, msg=massage)


    # test all urls inside the body tags
    def test_public_sign_up_urls_check(self):
        urls = self.app.post('/signup/', content_type='html/text')
        urls = str(urls.data)
        body_data = re.search('(<body>.*?</body>)', urls, re.DOTALL)
        urls = re.findall('href="(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"', str(body_data))

        for url in urls:
            path = url.split('"')
            rv = self.app.get(path[1], content_type='html/text', follow_redirects=True)
            self.assertEqual(rv.status_code, 200, msg=path)


    def test_password_match_sign_up(self):
        with self.app:
            rv = self.app.post('/signup/',
                               data=dict(
                                       username='johnsmith',
                                       email='john@smith.com',
                                       password='johnsmith',
                                       confirm='johnsmith'),
                               follow_redirects=True)
            massage = rv.data
            self.assertTrue(b'next page' in rv.data, msg=massage)


    # test for login page goes here
    def test_login_content(self):
        rv = self.app.get('/login/', content_type='html/text')
        self.assertTrue(b'login' in rv.data)


    def test_page_path_login(self):
        rv = self.app.get('/login/', content_type='html/text')
        self.assertEqual(rv.status_code, 200)


    # test all urls inside the body tags
    def test_public_login_urls_check(self):
        urls = self.app.get('/login/', content_type='html/text')
        urls = str(urls.data)
        body_data = re.search('(<body>.*?</body>)', urls, re.DOTALL)
        urls = re.findall('href="(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"', str(body_data))

        for url in urls:
            path = url.split('"')
            rv = self.app.get(path[1], content_type='html/text', follow_redirects=True)
            self.assertEqual(rv.status_code, 200, msg=path)


if __name__ == '__main__':
    unittest.main()
