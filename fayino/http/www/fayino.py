from flask import Flask, render_template, request, flash, redirect, session
from passlib.hash import sha256_crypt as crypt
from pymysql import escape_string as thwart

import sql_functions
from siteForms import AddressForm, Signup, Set_up_company

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jiugf098uhspuswfdsdN]LWX/,?RT'


# ####################      Testing Related Pages        ########################


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


# ####################      Login Related Pages        ########################


@app.route("/login/")
def login():
    return render_template("Login/login.html")


# ####################      Sign Up Related Pages        ########################

@app.route("/signUpCompleted/")
def signUpComplated():
    return render_template("SetUp/signUpCompleted.html")


@app.route("/confirmUserDetails/")
def confirmUserSetupDetails():
    user = sql_functions.get_uesr_details(session['userID'])
    company = sql_functions.get_company_details(session['companyID'])

    return render_template("SetUp/confirmDetails.html", user=user, company=company)


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

            # TODO remove the next flash statement
            flash(session['user'])
            flash('You are now signed up')
            return redirect('/companyDetails/')

        else:
            flash("The Email or user name you have entered has been used before", category='error')

        flash(signUpForm[3])
        return redirect('/')
    return render_template("SetUp/signup.html", form=form)


# ####################      Public Pages        ########################


@app.route('/')
@app.route('/home/')
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
