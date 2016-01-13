import datetime
import time

from cgi.person import Person
from cgi import database
from cgi.sql_scripts import insert_member


class Member(Person):
    """
    This class is used to hold the higher functions of the lower classes.
    """

    def __init__(self, foo):
        super().__init__(foo)
        self.schema = None
        if foo != 1:
            raise ValueError('foo is not equal to 1')

    def add_to_member_table(self, login_email, hashed_password, schema=None):
        """
        This function adds user to the members table so that they can login
        :param schema:
        :param login_email:
        :param hashed_password:
        :return:
        """
        accept_date = datetime.date.today()
        accept_date = str(accept_date.year) + "-" + str(accept_date.month) + "-" + str(accept_date.day)

        join_date = datetime.date.today()
        join_date = str(join_date.year) + "-" + str(join_date.month) + "-" + str(join_date.day)
        password_set = int(time.time())

        data = (login_email, hashed_password, accept_date, join_date, password_set)

        if schema is None:
            schema = self.schema

        db = database.Database(schema)
        try:
            db.execute(insert_member, data)
        finally:
            db.conn_close()

    @classmethod
    def create_member(cls, user_name, user_email, password, schema):
        """
        Add a user to the main database.
        :param schema:
        :param user_email:
        :param user_name:
        :param password:
        :return:
        """
        def add_to_member_table(login_email, hashed_password, use_schema=None):
            """
            This function adds user to the members table so that they can login
            :type use_schema: object
            :param use_schema:
            :param login_email:
            :param hashed_password:
            :return:
            """
            accept_date = datetime.date.today()
            accept_date = str(accept_date.year) + "-" + str(accept_date.month) + "-" + str(accept_date.day)

            join_date = datetime.date.today()
            join_date = str(join_date.year) + "-" + str(join_date.month) + "-" + str(join_date.day)
            password_set = int(time.time())

            data = (login_email, hashed_password, accept_date, join_date, password_set)

            db = database.Database(use_schema)
            try:
                db.execute(insert_member, data)
            finally:
                db.conn_close()

        def add_to_person_table():
            """
            This will and new person to the local person table
            """

        add_to_member_table(user_email, password, schema)
        add_to_person_table()



