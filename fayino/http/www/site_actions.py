from flask import request, session, flash

import siteForms
import sql_functions
from passlib.hash import sha256_crypt as crypt
from pymysql import escape_string as thwart


def login_action(form):

    if request.method == 'POST' and form.validate():
        user = thwart(form.userEmail.data())
        password = thwart(form.password.data())

        system_data = sql_functions.get_user_login_details(user)

        if crypt.verify(password, system_data[1]):
            return system_data, True


def check_session(email):

    check = session['user']
    if crypt.verify(email, check):
        count = session['count']
        session['count'] = 1 + int(count)

    else:
        session.clear()
        session['count'] = 1
        #TODO remove this flash massage only for testing
        flash('Values did not match')


class User(object):

    data = sql_functions.get_uesr_details(userID)

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

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
        return '<User %r>' % (self.nickname)