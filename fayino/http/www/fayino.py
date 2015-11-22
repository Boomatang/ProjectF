from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/home/')
def hello_world():
    return 'Hello World! This new'

if __name__ == '__main__':

    app.run(port=7000, debug=True)
