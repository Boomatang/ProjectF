import datetime

from flask import request, session, flash
import siteForms
import sql_functions
from sql_functions import conn_close, connection
from passlib.hash import sha256_crypt as crypt
from pymysql import escape_string as thwart


import string
from random import *


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
        # TODO remove this flash massage only for testing
        flash('Values did not match')


class User(object):
    """
    This is the user class all the details that maybe needed for a user should go in here.
    At a later date this will be used for the login manger too.
    """

    def __init__(self, login_details):
        self.data = sql_functions.get_user_details(login_details)

        self.id = self.data[0]
        self.first_name = self.data[1]
        self.last_name = self.data[2]
        self.username = self.data[3]

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
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Job(object):
    """
    The class that makes a job a job.
    More is to be added here and the time values should be called by functions the variable directly.
    """

    def __init__(self, job_number):
        self.data = sql_functions.get_job_details(job_number)
        self.title = self.data[0]
        self.description = self.data[1]
        self.data_block = self.data[2]
        self.pTime = self.data[3]
        self.pCost = self.data[4]
        self.job_number = self._format_job_number(job_number)
        self.job_number_sql = job_number
        self.total_time = self.get_times()

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
        # TODO work the time formatting, check pc for etxra
        return self.pTime

    def start_time_entry(self, userID):
        """
        Method to start the job in the database
        :param userID:
        :return:
        """
        start = datetime.datetime.now()

        sql = u'INSERT INTO job_time_log_TBL (' \
              u'jobIDyear, jobIDnum, personID, startTime) ' \
              u'VALUES (%s, %s, %s, %s)'
        data = (self.job_number_sql[0], self.job_number_sql[1], userID, start)

        c, conn = connection()
        c.execute(sql, data)
        conn_close(c, conn)

        return start

    def user_started_log(self, userID):
        """
        This function finds the  last time entry the user has started but not finished.
        This works on the bases that there will ever only be one entry that is has a finish time that is null for that user.
        :param userID:
        """

        sql = u'SELECT * ' \
              u'FROM job_time_log_TBL ' \
              u'WHERE personID = %s ' \
              u'AND jobIDyear = %s ' \
              u'AND jobIDnum = %s ' \
              u'AND finishTime IS NULL'

        data = (userID, self.job_number_sql[0], self.job_number_sql[1])

        c, conn = connection()
        c.execute(sql, data)

        value = c.fetchone()

        if value is not None:
            output = True

        else:
            output = False

        return output

    def user_stop_log(self, userID):
        """
        This function will stop the running job time.
        :param userID:
        """
        # TODO add in a fix to stop it trying to stop a job that is not running

        finish_time = datetime.datetime.now()

        sql = u'UPDATE job_time_log_TBL ' \
              u'SET finishTime = %s, ' \
              u'totalTime = %s ' \
              u'WHERE job_time_log_ID = %s'

        sql2 = u'SELECT job_time_log_ID, startTime ' \
               u'FROM job_time_log_TBL ' \
               u'WHERE personID = %s ' \
               u'AND jobIDyear = %s ' \
               u'AND jobIDnum = %s ' \
               u'AND finishTime IS NULL;'

        data2 = (userID, self.job_number_sql[0], self.job_number_sql[1])

        c, conn = connection()

        c.execute(sql2, data2)
        value = c.fetchone()
        if value is not None:
            time_ID = value[0]
            start = value[1]

            total_time = int(finish_time.strftime('%s')) - int(start.strftime('%s'))

            data = (finish_time, total_time, time_ID)
            c.execute(sql, data)

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
            pass
        else:
            sql = u'SELECT SUM(totalTime) ' \
                  u'FROM job_time_log_TBL ' \
                  u'WHERE jobIDyear = %s ' \
                  u'and jobIDnum = %s;'

            data = (self.job_number_sql[0], self.job_number_sql[1])

        c, conn = connection()

        c.execute(sql, data)
        time = c.fetchone()

        if time is not None:
            output = time[0]

        else:
            output = 0

        conn_close(c, conn)

        return output
