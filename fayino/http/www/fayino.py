from flask import Flask, render_template, request, flash, redirect, url_for
from siteForms import AddressForm, Signup
from pymysql import escape_string as thwart
from passlib.hash import sha256_crypt as crypt

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
    return render_template("testpage.html", form=form)




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
    return render_template("SetUp/confirmDetails.html")


@app.route('/companyDetails/')
def setCompanyDetails():
    return render_template("SetUp/setCompanyDetails.html")

from sql_functions import check_new_username_and_email, sign_up_user

@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    form = Signup(request.form)

    if request.method == 'POST' and form.validate():
        signUpForm = (thwart(form.user_name.data),
                      thwart(form.userEmail.data),
                      crypt.encrypt(thwart(form.password.data)),
                      thwart(str(form.accept_terms.data)))

        if check_new_username_and_email(signUpForm[0], signUpForm[1]):
            sign_up_user(signUpForm)

            flash('You are now signed up')

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
'''
@app.errorhandler(404)
def fail404(e):
    return render_template("Error/404.html")


@app.errorhandler(405)
def fail405(e):
    return render_template("Error/405.html")
'''

# #######################################################################

if __name__ == '__main__':

    app.run(port=7000, debug=True)
