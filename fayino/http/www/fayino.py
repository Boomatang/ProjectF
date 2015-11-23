from flask import Flask, render_template
app = Flask(__name__)

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


@app.route('/signup/')
def signup():
    return render_template("SetUp/signup.html")


# ####################      Public Pages        ########################


@app.route('/')
@app.route('/home/')
def publicHomePage():
    return render_template("Public-html/index.html")


# ####################      Error Pages        ########################
# TODO set up some basic error handing pages

@app.errorhandler(404)
def fail404(e):
    return render_template("Error/404.html")


@app.errorhandler(405)
def fail405(e):
    return render_template("Error/405.html")


# #######################################################################

if __name__ == '__main__':

    app.run(port=7000, debug=True)
