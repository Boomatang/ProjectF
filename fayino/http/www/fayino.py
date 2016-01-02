from functools import wraps

from flask import Flask, render_template, request, flash, redirect, session, url_for
from passlib.hash import sha256_crypt as crypt
from pymysql import escape_string as thwart
from wtforms import Form
# from flask_login import LoginManager, login_user, login_required, current_user
import siteForms
import sql_functions
from siteForms import AddressForm, Signup, Set_up_company
from site_actions import login_action, User, Job, password_gen

# ####################      Set up        ########################

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jiugf098uhspuswfdsdN]LWX/,?RT'


# login_manager = LoginManager()
# login_manager.init_app(app)


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

@app.route('/home/', methods=['POST', 'GET'])
@login_required
def private_home():
    user = User(session['login_details'], session['login_details']['person_ID'])
    assigned_jobs = []
    if user.assigned_jobs is not None:

        for job_number in user.assigned_jobs:
            job = Job(job_number, session['login_details'], user.id)
            assigned_jobs.append(job)

    form = Form(request.form)
    if request.method == 'POST' and assigned_jobs is not None:
        if sql_functions.verify_user_company_schema(session['login_details']):

            for jobs in assigned_jobs:
                if jobs.job_number in request.form:

                    if request.form[jobs.job_number] == 'Start':
                        start_time = jobs.start_time_entry(user.id)
                        flash(start_time.strftime('%Y/%m/%d %H:%M'))

                    elif request.form[jobs.job_number] == 'Stop':
                        finish_time = jobs.user_stop_log(user.id)
                        flash(finish_time.strftime('%Y/%m/%d %H:%M'))


    return render_template('private/index.html',
                           user=user,
                           assigned_jobs=assigned_jobs,
                           form=form)


# ####################      User Related Pages        ########################

@app.route('/user/<person_ID>', methods=['POST', 'GET'])
@login_required
def user_details(person_ID):
    """
    Bring the overview of all the details to show
    :param job_number:
    :return:
    """
    user = User(session['login_details'], person_ID)
    assigned_jobs = []
    if user.assigned_jobs is not None:

        for job_number in user.assigned_jobs:
            job = Job(job_number, session['login_details'], user.id)
            assigned_jobs.append(job)

    form = Form(request.form)
    if request.method == 'POST' and assigned_jobs is not None:
        if sql_functions.verify_user_company_schema(session['login_details']):

            for jobs in assigned_jobs:
                if jobs.job_number in request.form:

                    if request.form[jobs.job_number] == 'Start':
                        start_time = jobs.start_time_entry(user.id)
                        flash(start_time.strftime('%Y/%m/%d %H:%M'))

                    elif request.form[jobs.job_number] == 'Stop':
                        finish_time = jobs.user_stop_log(user.id)
                        flash(finish_time.strftime('%Y/%m/%d %H:%M'))


    return render_template('private/users/main_details.html',
                           user=user,
                           assigned_jobs=assigned_jobs,
                           form=form)


@app.route('/user/list/', methods=['POST', 'GET'])
@login_required
def all_user_list():

    # FIXME This page brakes if there is no jobs in the database
    """
    This page will show the list of the user in the company
    :return:
    """
    user_list = []
    number_list = sql_functions.get_all_user_ids(session['login_details'])

    for number in number_list:
        user_list.append(User(session['login_details'], number))

    return render_template('private/users/list.html', user_list=user_list)


@app.route('/user/review/<added_user>', methods=['POST', 'GET'])
@login_required
def user_review(added_user):
    new_user = User(session['login_details'], added_user)

    return render_template('private/users/review.html', new_user=new_user)


@app.route('/users/create', methods=['POST', 'GET'])
@login_required
def user_create():
    """
    The function lets a logged in user add more members to the company
    :return:
    """
    form = siteForms.CreateNewUser(request.form)
    user_name = sql_functions.get_sudo_username(session['login_details'])
    password = password_gen()

    if request.method == 'POST' and form.validate():
        new_user_name = thwart(form.user_name.data)
        first_name = thwart(form.first_name.data)
        last_name = thwart(form.last_name.data)
        email = thwart(form.userEmail.data)

        information = (new_user_name,
                       email,
                       first_name,
                       last_name,
                       crypt.encrypt(password))

        if sql_functions.check_new_username(new_user_name, session['login_details']):
            added_user = sql_functions.add_user(information, session['login_details'])
            return redirect(url_for('user_review', added_user=added_user))
        else:
            flash('User name and or email has been used before')

    return render_template('private/users/add.html',
                           form=form,
                           user_name=user_name,
                           password=password)


# ####################      Job Related Pages        ########################

@app.route('/jobs/<job_number>', methods=['POST', 'GET'])
@login_required
def job_main_details(job_number):
    """
    Bring the overview of all the details to show
    :param job_number:
    :return:
    """
    # TODO a lot of this code maybe able to be put in the Job Class
    # Job details
    year, number = job_number.split('-')

    job_number_sql = (int(year), int(number))

    job = Job(job_number_sql, session['login_details'])


    # assigned users
    member_list = []
    id_list = sql_functions.job_assigned_users(session['login_details'], job_number_sql)
    if id_list is not None:
        for id_value in id_list:
            member_list.append(User(session['login_details'], id_value))
    else:
        member_list = None

    # User list
    user_list = []
    number_list = sql_functions.get_all_user_ids(session['login_details'])

    for number in number_list:
        if number in id_list:
            pass
        else:
            user_list.append(User(session['login_details'], number))

    # page form details
    form = Form(request.form)
    if request.method == 'POST':
        if sql_functions.verify_user_company_schema(session['login_details']):
            user = session['login_details']['person_ID']

            if request.form['timer'] == 'Start':
                start_time = job.start_time_entry(user)
                flash(start_time.strftime('%Y/%m/%d %H:%M'))

            elif request.form['timer'] == 'Stop':
                finish_time = job.user_stop_log(user)
                flash(finish_time.strftime('%Y/%m/%d %H:%M'))

            elif request.form['timer'] == 'Assign':
                user_assigned = []

                for value in request.form:
                    for user in user_list:
                        if value == 'user'+str(user.id):
                            user_assigned.append(user.id)

                for user_id in user_assigned:
                    values = (job_number_sql[0], job_number_sql[1], user_id)

                    sql_functions.assign_users_to_job(values, session['login_details'])

            elif request.form['timer'] == 'Remove Members' and member_list is not None:
                remove_member = []
                for value in request.form:
                    for member in member_list:
                        if value == 'member'+str(member.id):
                            remove_member.append(member.id)

                for member_id in remove_member:
                    values = (job_number_sql[0], job_number_sql[1], member_id)

                    sql_functions.remove_users_from_job(values, session['login_details'])

        return redirect(url_for('job_main_details', job_number=job.job_number))

    return render_template('private/jobs/main_details.html',
                           job=job,
                           user_list=user_list,
                           member_list=member_list,
                           form=form)


@app.route('/jobs/', methods=['POST', 'GET'])
@login_required
def jobs_list():
    """
    Gives a list of all the jobs.
    Fillers will be added at a later date but for now this is all it does.
    """
    # FIXME This page brakes if there is no jobs in the database
    job_list = []
    number_list = sql_functions.get_all_job_numbers(session['login_details'])

    for number in number_list:
        job_list.append(Job(number, session['login_details']))

    return render_template('private/jobs/list.html', job_list=job_list)


@app.route('/newjoboverview/', methods=['POST', 'GET'])
@login_required
def new_job_overview():
    """
    Page gives a overview of the job that had been created in the page before hand
    :return:
    """
    job_number = session['temp_job_number']

    job = Job(job_number, session['login_details'])
    session.pop('temp_job_number', None)

    return render_template('private/jobs/jobOverView.html', job=job)


@app.route('/createNewJob/', methods=['POST', 'GET'])
@login_required
def create_job_page():
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

        job_number = sql_functions.create_job(values, session['login_details'])
        session['temp_job_number'] = job_number

        return redirect(url_for('new_job_overview'))

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
        data, confirm, = login_action(form)

        if confirm:
            company_schema = sql_functions.get_company_schema(data[2])
            person_ID = sql_functions.get_company_person_ID(data[0], company_schema)

            login_details = {'user_ID': data[0],
                             'company_ID': data[2],
                             'company_schema': company_schema,
                             'person_ID': person_ID}
            session.clear()
            session['login_details'] = login_details
            session['logged_in'] = True

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
def sign_up_completed():
    """
    This function forces the user to re-login to make user their details are in order.
    It will also clean up any left overs that may have been left in the session cookie.
    :return:
    """
    form = siteForms.LoginConfirm(request.form)
    if request.method == 'POST':
        data, confirm = login_action(form)

        if confirm:

            company_schema = sql_functions.get_company_schema(data[2])
            person_ID = sql_functions.get_company_person_ID(data[0], company_schema)

            login_details = {'user_ID': data[0],
                             'company_ID': data[2],
                             'company_schema': company_schema,
                             'person_ID': person_ID}
            session.clear()
            session['login_details'] = login_details
            session['logged_in'] = True

            flash('Logged in successfully.')
            return redirect('/home/')

        else:
            flash('Login details did not match.')

    return render_template("SetUp/signUpCompleted.html", form=form)


@app.route("/confirmUserDetails/")
def confirm_user_setup_details():
    # Setup company schema for user
    # Add the user to the company schema

    if sql_functions.verify_user_company_schema(session['login_details']):
        # create the required tables for the schema
        # Setup company schema for user
        company_schema = session['login_details']['company_schema']
        sql_functions.create_company_schema(company_schema)
        sql_functions.create_company_schema_tables(company_schema)

        # Add the user to the company schema
        person_ID = sql_functions.add_user_to_company_member_tbl(session['login_details'],
                                                                 session['temp_user_details'][1])

        session['login_details']['person_ID'] = person_ID

    user = User(session['login_details'])

    return render_template("SetUp/confirmDetails.html",
                           user=user)


@app.route('/companyDetails/', methods=['POST', 'GET'])
def set_company_details():
    """
    Sets up the new company for the user that has just made an account
    :return:
    """
    # TODO If the user makes account but try not set a company up they should be forced to do so.
    form = Set_up_company(request.form)

    if request.method == 'POST' and form.validate():
        company = thwart(form.company_name.data)

        company_ID, company_schema = sql_functions.enter_company_detail(company)

        sql_functions.link_user_company(session['temp_user_details'][0], company_ID)

        login_details = {'user_ID': session['temp_user_details'][0],
                         'company_ID': company_ID,
                         'company_schema': company_schema,
                         'person_ID': ''}

        session['login_details'] = login_details

        return redirect(url_for('confirm_user_setup_details'))

    return render_template("SetUp/setCompanyDetails.html", form=form)


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    # fixme there is no way to roll back to this page if the company works wrong. Need a role back function on the database
    """
    This uses the new database layout and will sign a new user up with an account
    :return:
    """
    form = Signup(request.form)

    if request.method == 'POST' and form.validate():
        sign_up_form = (thwart(form.user_name.data),
                        thwart(form.userEmail.data),
                        crypt.encrypt(thwart(form.password.data)),
                        thwart(str(form.accept_terms.data)))

        userID = sql_functions.sign_up_user(sign_up_form)
        session.clear()
        session['temp_user_details'] = (userID, sign_up_form[0])

        flash('You are now signed up')
        return redirect(url_for('set_company_details'))

    return render_template("SetUp/signup.html", form=form)


# ####################      Public Pages        ########################


@app.route('/')
def publicHomePage():
    return render_template("Public-html/index.html")


# ####################      Error Pages        ########################
# TODO set up some basic error handing pages

@app.route('/not_built/')
def not_built():
    return render_template('error/not_built.html')


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
