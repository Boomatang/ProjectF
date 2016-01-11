from flask import Flask
# ####################      Set up        ########################

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jiugf0983yX R~XHH!jiugf098uhspuswfdsdN]LWX/,?RT'


@app.route('/')
def index():
    return u'Hello World'


# #######################################################################

if __name__ == '__main__':
    app.run(port=7070, debug=True)