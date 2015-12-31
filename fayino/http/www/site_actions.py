from flask import request, session, flash
import siteForms
import sql_functions
from passlib.hash import sha256_crypt as crypt
from pymysql import escape_string as thwart


def login_action(form):
    if request.method == 'POST' and form.validate():
        user = thwart(form.userEmail.data)
        password = thwart(form.password.data)

        system_data = sql_functions.get_user_login_details(user)

        if crypt.verify(password, system_data[1]):
            return system_data, True, user


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
    def __init__(self, userID):
        self.data = sql_functions.get_uesr_details(userID)

        self.id = self.data[0]
        self.email = self.data[9]
        self.username = self.data[3]
        self.f_name = self.data[1]
        self.l_name = self.data[2]

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

