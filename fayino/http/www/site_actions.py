import datetime
import string
from random import *

from flask import request, session
from passlib.hash import sha256_crypt as crypt
from pymysql import escape_string as thwart

import sql_functions
from sql_functions import conn_close, connection, verify_user_company_schema


def password_gen(min_char=8, max_char=14):
    all_char = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(all_char) for x in range(randint(min_char, max_char)))

    return password


def login_action(form):
    if request.method == 'POST' and form.validate():
        user = thwart(form.userEmail.data)
        password = thwart(form.password.data)

        system_data = sql_functions.get_possible_user_login_details(user)

        for value in system_data:
            if crypt.verify(password, value[1]):
                return value, True


def check_session(email):
    check = session['user']
    if crypt.verify(email, check):
        if 'count' in session:
            count = session['count']
        else:
            count = 0
        session['count'] = 1 + int(count)

    else:
        session.clear()
        session['count'] = 1


class User(object):
    """
    This is the user class all the details that maybe needed for a user should go in here.
    At a later date this will be used for the login manger too.
    """

    def __init__(self, login_details, user_ID=None):
        self.login_details = login_details
        if user_ID is None:
            self.data = sql_functions.get_user_details(self.login_details)
        else:
            self.login_details['person_ID'] = user_ID
            self.login_details['user_ID'] = sql_functions.get_local_master_ID(user_ID, login_details)

            self.data = sql_functions.get_user_details(self.login_details)

        self.id = self.data[0]
        self.first_name = self.data[1]
        self.last_name = self.data[2]
        self.username = self.data[3]

        self.default_email = self.get_default_email()
        self.assigned_jobs = self.get_assigned_jobs()
        self.jobs_list = self.jobs_worked_on()

    def jobs_worked_on(self):
        """
        This returns a list of all the jobs a user has worked on
        :return:
        """
        output = None
        sql = u'SELECT DISTINCT job_ID_year, job_ID_number ' \
              u'FROM job_time_log_TBL ' \
              u'WHERE person_ID = %s'

        if verify_user_company_schema(self.login_details):
            c, conn = connection(self.login_details['company_schema'])

            try:
                c.execute(sql, self.id)
                value = c.fetchall()

                if value is not None:
                    output = value
            finally:
                conn_close(c, conn)

            return output

    def job_times(self, job_id=None):

        """
        returns the time that has been spent on all jobs or just the one.
        :param job_id:
        """
        # TODO add in the function to check between dates
        time = 0
        if job_id is not None:
            sql = u'SELECT SUM(total_time) ' \
                  u'FROM job_time_log_TBL ' \
                  u'WHERE person_ID = %s ' \
                  u'AND job_ID_year = %s ' \
                  u'AND job_ID_number = %s '

            data = (self.id, job_id[0], job_id[1])

        else:

            sql = u'SELECT SUM(total_time) ' \
                  u'FROM job_time_log_TBL ' \
                  u'WHERE person_ID = %s'
            data = (self.id,)

        if verify_user_company_schema(self.login_details):
            c, conn = connection(self.login_details['company_schema'])

            try:
                c.execute(sql, data)
                value = c.fetchone()

                if value is not None:
                    time = value[0]
            finally:
                conn_close(c, conn)

            return time

    def get_default_email(self):
        """
        Function gets the default email address for the user
        :return: an email address
        """
        email = 'error@error.error'
        sql = u'SELECT detail ' \
              u'FROM communication_TBL ' \
              u'WHERE person_ID = %s ' \
              u'AND main = 1 ' \
              u'AND communication_type = "email"'
        data = (self.login_details['person_ID'])

        if verify_user_company_schema(self.login_details):
            c, conn = connection(self.login_details['company_schema'])

            try:
                c.execute(sql, data)
                value = c.fetchone()

                if value is not None:
                    email = value[0]
            finally:
                conn_close(c, conn)
        return email

    def get_assigned_jobs(self):

        """
        Gets any jobs that may have been assigned to the user
        :return: returns a list if true else None
        """
        output = None
        sql = u'SELECT job_ID_year, job_ID_number ' \
              u'FROM member_linked_jobs_TBL ' \
              u'WHERE person_ID = %s'

        data = (self.id,)

        if verify_user_company_schema(self.login_details):
            c, conn = connection(self.login_details['company_schema'])

            try:
                c.execute(sql, data)
                values = c.fetchall()

                if values is not None:
                    output = values
            finally:
                conn_close(c, conn)

        return output

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(1)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Job(object):
    """
    The class that makes a job a job.
    More is to be added here and the time values should be called by functions the variable directly.
    """

    def __init__(self, job_number, login_details, user_id=None):
        self.data = sql_functions.get_job_details(job_number, login_details)
        self.title = self.data[0]
        self.description = self.data[1]
        self.data_block = self.data[2]
        self.pTime = self.data[3]
        self.pCost = self.data[4]
        self.job_number = self._format_job_number(job_number)
        self.job_number_sql = job_number
        self.company_schema = login_details['company_schema']
        self.total_time = self.get_times()
        self.user_view_running = self.user_started_log(user_id)
        self.timed_user_ids = self.user_with_time()

    @staticmethod
    def _format_job_number(job):
        """
        create a string format for the job number there is no other use for this method and is required by nothing other than this class.
        :param job:
        :return:
        """
        year = str(job[0])
        number = job[1]
        if number < 10:
            string_number = '00' + str(number)
        elif number < 100:
            string_number = '0' + str(number)
        else:
            string_number = str(number)

        string_job_number = year + '-' + string_number

        return string_job_number

    def quoted_time(self):
        # TODO work the time formatting, check pc for extra
        return self.pTime

    def user_with_time(self):
        """
        The list that is returned is a distinct list of user that have time to the job
        :return:
        """
        output = None
        sql = u'SELECT DISTINCT person_ID ' \
              u'FROM job_time_log_TBL ' \
              u'WHERE job_ID_year = %s ' \
              u'AND job_ID_number = %s '

        c, conn = connection(self.company_schema)
        try:
            c.execute(sql, self.job_number_sql)
            values = c.fetchall()

            if values:
                output = values
        finally:
            conn_close(c, conn)
        return output

    def start_time_entry(self, userID):
        """
        Method to start the job in the database
        :param userID:
        :return:
        """
        start = datetime.datetime.now()

        sql = u'INSERT INTO job_time_log_TBL (' \
              u'job_ID_year, job_ID_number, person_ID, start_time) ' \
              u'VALUES (%s, %s, %s, %s)'
        data = (self.job_number_sql[0], self.job_number_sql[1], userID, start)

        c, conn = connection(self.company_schema)
        try:
            c.execute(sql, data)
        finally:
            conn_close(c, conn)

        return start

    def user_started_log(self, userID):
        """
        This function finds the last time entry the user has started but not finished.
        This works on the bases that there will ever only be one entry that is has a finish time that is null for that user.
        :param userID:
        """
        output = None
        sql = u'SELECT * ' \
              u'FROM job_time_log_TBL ' \
              u'WHERE person_ID = %s ' \
              u'AND job_ID_year = %s ' \
              u'AND job_ID_number = %s ' \
              u'AND finish_time IS NULL'

        data = (userID, self.job_number_sql[0], self.job_number_sql[1])
        if userID is not None:
            c, conn = connection(self.company_schema)
            try:
                c.execute(sql, data)

                value = c.fetchone()

                if value is not None:
                    output = True

                else:
                    output = False
            finally:
                conn_close(c, conn)
        return output

    def user_stop_log(self, userID):
        """
        This function will stop the running job time.
        :param userID:
        """
        # TODO add in a fix to stop it trying to stop a job that is not running

        finish_time = datetime.datetime.now()

        sql = u'UPDATE job_time_log_TBL ' \
              u'SET finish_time = %s, ' \
              u'total_time = %s ' \
              u'WHERE job_time_log_ID = %s'

        sql2 = u'SELECT job_time_log_ID, start_time ' \
               u'FROM job_time_log_TBL ' \
               u'WHERE person_ID = %s ' \
               u'AND job_ID_year = %s ' \
               u'AND job_ID_number = %s ' \
               u'AND finish_time IS NULL;'

        data2 = (userID, self.job_number_sql[0], self.job_number_sql[1])

        c, conn = connection(self.company_schema)
        try:
            c.execute(sql2, data2)
            value = c.fetchone()
            if value is not None:
                time_ID = value[0]
                start = value[1]

                total_time = int(finish_time.strftime('%s')) - int(start.strftime('%s'))

                data = (finish_time, total_time, time_ID)
                c.execute(sql, data)
        finally:
            conn_close(c, conn)

        return finish_time

    def get_times(self, user_ID=None, start_date=None, finish_date=None):
        """
        Used to get the times of the job.
        It will get the total time and at a later date be able to do user and date refines.
        This function should find the values for the entry's that have been started but not yet finished.
        These non finished entry's should be added to the total time
        :param start_date:
        :param finish_date:
        :param user_ID:
        """
        if user_ID is not None:
            sql = u'SELECT SUM(total_time) ' \
                  u'FROM job_time_log_TBL ' \
                  u'WHERE job_ID_year = %s ' \
                  u'AND job_ID_number = %s ' \
                  u'AND person_ID = %s;'

            data = (self.job_number_sql[0], self.job_number_sql[1], user_ID)
        else:
            sql = u'SELECT SUM(total_time) ' \
                  u'FROM job_time_log_TBL ' \
                  u'WHERE job_ID_year = %s ' \
                  u'and job_ID_number = %s;'

            data = (self.job_number_sql[0], self.job_number_sql[1])

        c, conn = connection(self.company_schema)
        try:
            c.execute(sql, data)
            time = c.fetchone()

            if time is not None:
                output = time[0]

            else:
                output = 0
        finally:
            conn_close(c, conn)

        return output

    def __repr__(self):
        return '<Job: %r>' % (self.title)


class ClientCompany(object):
    """
    This class is for the company. Its the new style from me.

    ALl values should be passed in with a dict that has the following format.
    *** values input dict ***

    'name': '',
    'code': '',
    'ID': 0,
    'comm': [{}]
    'address': [{}]

    The comm {} format is
        'detail':'',
        'main': 0,
        'type': ''

    The address {} format is
        'line1': '',
        'line2': '',
        'town': '',
        'county': '',
        'country': '',
        'postcode':'',
        'billing': 0
        'default: 0'
    *************************
    """

    def __init__(self, client_id, login_details, data_set=None):

        """
        This is the setting function
        :type login_details: Standard
        """
        self.schema = login_details['company_schema']
        data = self.get_details(client_id)
        self.name = data[1]
        self.id = data[0]
        self.sort_code = data[2]
        self.data_set = data_set

    def get_details(self, client_id):
        sql = u'SELECT client_company_ID, name, sort_code ' \
              u'FROM client_company_TBL ' \
              u'WHERE client_company_ID = %s'

        data = (client_id,)
        output = None
        c, conn = connection(self.schema)
        try:
            c.execute(sql, data)
            value = c.fetchone()
            if value is not None:
                output = value
        finally:
            conn_close(c, conn)

        return output


    def add_communication(self, values=None):
        """
        Add a communication entry is added here. This could be email, phone or fax
        The values should be a dict
        :param values: Should be a dict
        """

        if values is None:
            values = self.data_set['comm']
        c, conn = connection(self.schema)

        sql = u'INSERT INTO communication_TBL ' \
              u'(detail, main, client_company_ID, communication_type) ' \
              u'VALUES (%s, %s, %s, %s);'

        try:
            for comm in values:
                if len(comm['detail']) == 0:
                    pass
                else:
                    data = (comm['detail'], comm['main'], self.id, comm['type'])
                    c.execute(sql, data)
        finally:
            conn_close(c, conn)

    def add_address(self, address_list=None):
        """
        Here we are adding an address there can be more than one but only one default
        :param client_id:
        :param address:
        """
        sql = u' INSERT INTO address_TBL ' \
              u'(line_1, line_2, city, county, country, billing_address, main_address, client_company_ID) ' \
              u'VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
        if address_list is None:
            address_list = self.data_set['address']

        c, conn = connection(self.schema)

        try:
            for address in address_list:
                if address['line_2'] is None:
                    address['line_2'] = 'NULL'
                if address['billing'] is None:
                    address['billing'] = 0
                if address['default'] is None:
                    address['default'] = 0

                data = (address['line_1'],
                        address['line_2'],
                        address['city'],
                        address['county'],
                        address['country'],
                        address['billing'],
                        address['default'],
                        self.id)

                c.execute(sql, data)
        finally:
            conn_close(c, conn)


    @classmethod
    def create_client(cls, values, login_details):
        """
        This function will construct the company if it does not exist in the client company database.
        It will do this by magic
        :param login_details: Common across all settings
        :param values: Values used to set up client
        """
        client_id = None
        c, conn = connection(login_details['company_schema'])

        def sort_code_unique(sort_code):
            """
            Checks to see if the sort_code is Unique
            :param sort_code:
            """
            output = False
            sql = u'SELECT sort_code ' \
                  u'FROM client_company_TBL ' \
                  u'WHERE sort_code = %s;'
            data = (sort_code,)
            c.execute(sql, data)
            test = c.fetchone()

            if test is None:
                output = True

            return output

        def add_client(name, sort_code):
            """
            Adds the client to the client company table in the user company database
            :param name: String name of the client company
            :param sort_code: String sort code for the client company
            """

            sql = u'INSERT INTO client_company_TBL ' \
                  u'(name, sort_code) ' \
                  u'VALUES (%s, %s);'
            data = (name, sort_code)
            c.execute(sql, data)
            conn.commit()

        def get_client_id(name, sort_code):
            """
            Will return the ID for the client company that has just been added
            :param name:
            :param sort_code:
            """
            output = None

            sql = u'SELECT client_company_ID ' \
                  u'FROM client_company_TBL ' \
                  u'WHERE name = %s ' \
                  u'AND sort_code = %s'

            data = (name, sort_code)
            c.execute(sql, data)
            value = c.fetchone()
            if value is not None:
                output = value[0]

            return output

        try:
            if sort_code_unique(values['code']):
                add_client(values['name'], values['code'])
                client_id = get_client_id(values['name'], values['code'])
        finally:
            conn_close(c, conn)
        return cls(client_id, login_details)

    def __repr__(self):
        return '<Client Company: %r>' % (self.name,)
