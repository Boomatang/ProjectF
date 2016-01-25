"""
This module holds the class for the person. A person is someone that makes up other classes.
This class will be blank for some time but will be filled out as we go along
"""
import datetime

from cgi import database


class Person(object):
    """
    This class is used to hold the higher functions of the lower classes.
    """

    def __init__(self, foo, db_schema):

        if db_schema is not None:
            self.db = database.Database(db_schema)


        if foo != 1:
            raise ValueError('foo is not equal to 1')

    def add_person(self, username, schema, master_id=None):
        db = database.Database(schema)
        if master_id is not None:
            sql = u'INSERT INTO member_TBL ' \
                  u'(username, join_date, accept_terms, login_master_ID) ' \
                  u'VALUES (%s, %s, %s, %s);'

            set_up_date = datetime.date.today()
            set_up_date = str(set_up_date.year) + \
                          "-" + str(set_up_date.month) + \
                          "-" + str(set_up_date.day)

            data = (username, set_up_date, set_up_date, master_id)

            db.execute(sql, data)
            db.conn_close()

    def get_id_by_username(self, username, current_schema=None):
        if current_schema is not None:
            db = database.Database(current_schema)
        else:
            db = self.db

        sql = u'SELECT person_ID ' \
              u'FROM member_TBL ' \
              u'WHERE username = %s'

        data = (username,)

        value = db.return_values(sql, data)

        return value
