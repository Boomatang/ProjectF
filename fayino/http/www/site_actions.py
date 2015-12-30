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
        #TODO remove this flash massage only for testing
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

    def __init__(self, job_number):
        self.data = sql_functions.get_job_details(job_number)

