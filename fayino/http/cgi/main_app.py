from flask import Flask, render_template, request, flash, session
from pymysql import escape_string as thwart
from passlib.hash import sha256_crypt as crypt


# ####################      Set up        ########################
from wtforms import Form

from cgi import member
from cgi import site_forms
from cgi import company

app = Flask(__name__, template_folder='../templates', static_folder='../www/static/')

app.secret_key = 'A0Zr98j/3yX R~XHH!jiugf0983yX R~XHH!jiugf098uhspuswfdsdN]LWX/,?RT'


@app.route('/login/')
def login():
    return 'login'


@app.route('/signup/', methods=['POST', 'GET'])
def sign_up():

    form = site_forms.Signup(request.form)
    if request.method == 'POST' and form.validate():

        name = thwart(form.username.data)
        email = thwart(form.email.data)
        password = thwart(form.password.data)
        re_password = thwart(form.confirm.data)
        company_name = thwart(form.company_name.data)

        if password == re_password:
            # TODO hash password
            password = crypt.encrypt(password)
            new_company = company.Company.enter_company_detail(company_name)
            user = member.Member.create_member(name, email, password, new_company.id, new_company.schema)

            session['company'] = new_company.id
            session['user'] = user.id
            return 'next page'
        else:
            flash('Passwords do not match', 'error')
            return render_template('sign_up/sign_up_form.html', form=form)

    return render_template('sign_up/sign_up_form.html', form=form)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('public/index.html')


# #######################################################################

if __name__ == '__main__':
    app.run(port=7070, debug=True)