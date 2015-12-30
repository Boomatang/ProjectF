from functools import wraps

from flask import Flask, render_template, request, flash, redirect, session
from passlib.hash import sha256_crypt as crypt
from pymysql import escape_string as thwart
#from flask_login import LoginManager, login_user, login_required, current_user
import siteForms
import sql_functions
from siteForms import AddressForm, Signup, Set_up_company
from site_actions import login_action, check_session, User


# ####################      Set up        ########################

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jiugf098uhspuswfdsdN]LWX/,?RT'
#login_manager = LoginManager()
#login_manager.init_app(app)


# ####################      wrappers        ########################

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get_id(current_user)


# ####################      Testing Related Pages        ########################

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login in first..')
            return redirect('/login/')

    return wrap


@app.route("/testing/", methods=['GET', 'POST'])
def testing():
    form = AddressForm(request.form)

    if request.method == 'POST' and form.validate():
        address = (form.address_line1.data,
                   form.address_line2.data,
                   form.address_town.data,
                   form.address_county.data,
                   form.address_country.data,
                   form.address_postcode.data,
                   form.address_type.data,
                   form.address_default.data)
        flash(address)
        return redirect('/')
    return render_template("jinja/child.html", form=form)


# ####################      Private Related Pages        ########################

@app.route('/home/')
@login_required
def private_home():
    return render_template('private/index.html')


# ####################      Job Related Pages        ########################

@app.route('/createNewJob', methods=['POST', 'GET'])
@login_required
def CreateJobPage():

    """
    Code to make a job in the basic form is here
    :return:
    """
    form = siteForms.JobCreate(request.form)
    if request.method == 'POST':
        title = thwart(form.name.data)
        description = thwart(form.description.data)
        cost = thwart(str(form.pCost.data))
        length = thwart(str(form.pTime.data))

        values = [title, description, cost, length]

        job_number = sql_functions.create_job(values)

        flash(values)
        flash(job_number)

    return render_template('private/jobs/create.html', form=form)



# ####################      Login Related Pages        ########################

@app.route("/logout/")
@login_required
def logout():
    """
    Should log a user out with out removing any session cookie inform.
    This may need to be updated at a later date.
    :return: Goes back to the public home page
    """
    session.pop('logged_in', None)

    flash('You have been logged out')
    return redirect('/')


@app.route("/login/", methods=['POST', 'GET'])
def login():
    session.clear()
    form = siteForms.LoginConfirm(request.form)
    if request.method == 'POST':
        data, confirm, input_email = login_action(form)

        if confirm:
            #check_session(input_email)
            user = User(data[0])

            session['user'] = user.id
            session['logged_in'] = True

            #login_user(user)

            flash('Logged in successfully.')
            return redirect('/home/')

        else:
            flash('Login details did not match.')

    return render_template("Login/login.html", form=form)


# ####################      Sign Up Related Pages        ########################

@app.route('/editSignUp/')
def editSignUp():
    return render_template('Setup/editDetails.html')


@app.route("/signUpCompleted/", methods=['POST', 'GET'])
def signUpComplated():

    form = siteForms.LoginConfirm(request.form)
    if request.method == 'POST':
        data, confirm, input_email = login_action(form)

        if confirm:
            check_session(input_email)
            user = User(data[0])

            session['user'] = user.id
            session['logged_in'] = True

            #login_user(user)

            flash('Logged in successfully.')
            return redirect('/home/')

        else:
            flash('Login details did not match.')

    return render_template("SetUp/signUpCompleted.html", form=form)


@app.route("/confirmUserDetails/")
def confirmUserSetupDetails():

    user = sql_functions.get_uesr_details(session['userID'])
    company = sql_functions.get_company_details(session['companyID'])

    user_data = {'userName': user[3],
                 'email': user[9],
                 'password': '******',
                 'companyName': company[1],
                 'companyShort': company[2]}

    return render_template("SetUp/confirmDetails.html",
                           user_data=user_data)


@app.route('/companyDetails/', methods=['POST', 'GET'])
def setCompanyDetails():
    form = Set_up_company(request.form)

    if request.method == 'POST' and form.validate():
        companyID = sql_functions.next_companyID()
        company = (thwart(form.company_name.data),
                   thwart(form.company_code.data),
                   thwart(form.company_type.data),
                   session['userID'],
                   companyID)

        if sql_functions.company_code_check(company[1]):

            sql_functions.enter_company_detail(company)
            sql_functions.link_user_company(company[3], company[4])
            session['companyID'] = company[4]
            return redirect('/confirmUserDetails/')

        else:
            flash("That company short code has been taken..",
                  category='error')

    return render_template("SetUp/setCompanyDetails.html", form=form)


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    # fixme there is no way to roll back to this page if the company works wrong. Need a role back function on the database
    form = Signup(request.form)

    if request.method == 'POST' and form.validate():
        signUpForm = (thwart(form.user_name.data),
                      thwart(form.userEmail.data),
                      crypt.encrypt(thwart(form.password.data)),
                      thwart(str(form.accept_terms.data)))

        if sql_functions.check_new_username_and_email(signUpForm[0], signUpForm[1]):
            userID = sql_functions.sign_up_user(signUpForm)

            session['user'] = crypt.encrypt(signUpForm[1])
            session['userID'] = userID

            flash('You are now signed up')
            return redirect('/companyDetails/')

        else:
            flash("The Email or user name you have entered has been used before", category='error')

        flash(signUpForm[3])
        return redirect('/')
    return render_template("SetUp/signup.html", form=form)


# ####################      Public Pages        ########################


@app.route('/')
def publicHomePage():
    return render_template("Public-html/index.html")


# ####################      Error Pages        ########################
# TODO set up some basic error handing pages

@app.errorhandler(404)
def fail404(e):
    return render_template("error/error404.html")


'''
@app.errorhandler(405)
def fail405(e):
    return render_template("Error/405.html")
'''

# #######################################################################

if __name__ == '__main__':
    app.run(port=7000, debug=True)
