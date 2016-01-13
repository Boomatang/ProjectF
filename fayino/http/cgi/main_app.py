from flask import Flask, render_template

# ####################      Set up        ########################

app = Flask(__name__, template_folder='../templates', static_folder='../www/static/')

app.secret_key = 'A0Zr98j/3yX R~XHH!jiugf0983yX R~XHH!jiugf098uhspuswfdsdN]LWX/,?RT'


@app.route('/login/')
def login():
    return 'login'


@app.route('/signup/')
def sign_up():
    return 'Sign up'


@app.route('/')
def index():
    return render_template('public/index.html')


# #######################################################################

if __name__ == '__main__':
    app.run(port=7070, debug=True)