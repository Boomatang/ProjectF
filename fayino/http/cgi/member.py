import datetime
import time

from flask import session

from cgi.person import Person
from cgi import database
from cgi.sql_scripts import insert_member


class Member(Person):
    """
    This class is used to hold the higher functions of the lower classes.
    """

    def __init__(self, schema, current_id):
        super().__init__(1, db_schema=schema)
        self.schema = None
        self.id = current_id

    def add_to_member_table(self, login_email, hashed_password, company, schema=None):
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

        data = (login_email, hashed_password, accept_date, join_date, password_set, company)

        if schema is None:
            schema = self.schema

        db = database.Database(schema)
        try:
            db.execute(insert_member, data)
        finally:
            db.conn_close()

    @classmethod
    def create_member(cls, user_name, user_email, password, new_company_id, schema):
        """
        Add a user to the main database.
        :param new_company_id:
        :param schema:
        :param user_email:
        :param user_name:
        :param password:
        :return:
        """
        def add_to_member_table(login_email, hashed_password, company_id):
            """
            This function adds user to the members table so that they can login
            :param company_id:
            :param login_email:
            :param hashed_password:
            :return:
            """
            accept_date = datetime.date.today()
            accept_date = str(accept_date.year) + "-" + str(accept_date.month) + "-" + str(accept_date.day)

            join_date = datetime.date.today()
            join_date = str(join_date.year) + "-" + str(join_date.month) + "-" + str(join_date.day)
            password_set = int(time.time())

            data = (login_email, hashed_password, accept_date, join_date, password_set, company_id)

            db = database.Database('test_login_master_files')
            try:
                db.execute(insert_member, data)
            finally:
                db.conn_close()

        def add_to_person_table(username, email, current_schema, master_id=None):
            """
            This will and new person to the local person table
            :param master_id:
            :param current_schema:
            :param email:
            :param username:
            """
            if master_id is not None:
                Person.add_person(username, current_schema, master_id)
                user_id = Person.get_id_by_username(username, current_schema)
                return user_id
            else:
                pass

        add_to_member_table(user_email, password, new_company_id)
        current_user = add_to_person_table(user_name, user_email, schema)

        return cls(current_user, schema)

