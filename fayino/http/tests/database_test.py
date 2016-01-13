import unittest
from cgi.database import Database
from cgi.tables import sql as tables


class DatabaseTests(unittest.TestCase):
    """
    testing the database module
    """
    def setUp(self):
        self.fay = Database('fayino')
        self.fay.execute('CREATE SCHEMA `default_account`;')
        self.fay.conn.commit()
        self.d = Database('default_account')

    def tearDown(self):
        self.d.conn_close()
        self.fay.execute('DROP DATABASE `default_account`;')
        self.fay.conn.commit()
        self.fay.conn_close()

    # test that a connection can be made
    def test_connection(self):
        self.failureException(Database.connection('default_account'))

    # Creates the tables for a default account
    def test_create_tables(self):
        self.assertIsNot(self.d.create_tables(tables), False)
