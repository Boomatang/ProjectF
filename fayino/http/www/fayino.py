import datetime
from functools import wraps
from wtforms import Form
from flask import Flask, render_template, request, flash, redirect, session, url_for
from passlib.hash import sha256_crypt as crypt
from pymysql import escape_string as thwart
#from flask_login import LoginManager, login_user, login_required, current_user
import siteForms
import sql_functions
from siteForms import AddressForm, Signup, Set_up_company
from site_actions import login_action, check_session, User, Job, password_gen


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


# ####################      User Related Pages        ########################

@app.route('/user/review/', methods=['POST', 'GET'])
@login_required
def user_review():
    return render_template('private/user/review.html')


@app.route('/users/create', methods=['POST', 'GET'])
@login_required
def user_create():

    form = siteForms.CreateNewUser(request.form)
    user_name = sql_functions.get_sudo_username()
    password = password_gen()

    if request.method == 'POST' and form.validate():
        new_user_name = thwart(form.user_name.data)
        first_name = thwart(form.first_name.data)
        last_name = thwart(form.last_name.data)
        email = thwart(form.userEmail.data)
        acceptDate = datetime.date.today()
        acceptDate = str(acceptDate.year) + "-" + str(acceptDate.month) + "-" + str(acceptDate.day)

        information = (new_user_name,
                       email,
                       first_name,
                       last_name,
                       crypt.encrypt(password))

        if sql_functions.check_new_username_and_email(new_user_name, email):
            sql_functions.add_user(information)
            return redirect('/user/review/')
        else:
            flash('User name and or email has been used before')

    return render_template('private/users/add.html',
                           form=form,
                           user_name=user_name,
                           password=password)

# ####################      Job Related Pages        ########################

@app.route('/jobs/<job_number>',  methods=['POST', 'GET'])
@login_required
def job_main_details(job_number):

    """
    Bring the overview of all the details to show
    :param job_number:
    :return:
    """

    year, number = job_number.split('-')

    job_number_sql = (int(year), int(number))

    job = Job(job_number_sql)

    form = Form(request.form)
    if request.method == 'POST':
        user = session['user']

        if request.form['timer'] == 'Start':
            start_time = job.start_time_entry(user)
            flash(start_time.strftime('%Y/%m/%d %H:%M'))
            flash(user)

        elif request.form['timer'] == 'Stop':
            finish_time = job.user_stop_log(user)
            flash(finish_time.strftime('%Y/%m/%d %H:%M'))

            flash(user)

        return redirect(url_for('job_main_details', job_number=job.job_number))

    return render_template('private/jobs/main_details.html', job=job, form=form)


@app.route('/jobs/',  methods=['POST', 'GET'])
@login_required
def jobs_list():
    """
    Gives a list of all the jobs.
    Fillers will be added at a later date but for now this is all it does.
    """
    job_list = []
    number_list = sql_functions.get_all_job_numbers()

    for number in number_list:
        job_list.append(Job(number))

    return render_template('private/jobs/list.html', job_list=job_list)


@app.route('/newjoboverview/',  methods=['POST', 'GET'])
@login_required
def new_job_overview():

    """
    Page gives a overview of the job that had been created in the page before hand
    :return:
    """
    job_number = session['temp_job_number']

    job = Job(job_number)
    session.pop('temp_job_number', None)

    return render_template('private/jobs/jobOverView.html', job=job)


@app.route('/createNewJob/', methods=['POST', 'GET'])
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
        session['temp_job_number'] = job_number

        return redirect('/newjoboverview/')

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
