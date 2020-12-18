from flask import *
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os.path import join, dirname, realpath
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from random_genre import random_genre
from flask_moment import Moment
import os
from os import environ, path
from dotenv import load_dotenv
import flask_praetorian

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

app = Flask(__name__)
app.config.from_object(environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
moment = Moment(app)
credential = ServiceAccountCredentials.from_json_keyfile_name(join(dirname(realpath(__file__)), 'ursas.json'),
                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",
                                                               "https://www.googleapis.com/auth/drive"])
cors = CORS(app, resources={r'/*': {"origins": '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'
mail = Mail(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

db = SQLAlchemy(app)
guard = flask_praetorian.Praetorian()

from models import Post, User

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def send_email(email, subject, name, message):
    msg = Message(subject, sender='ursaminorsweb@gmail.com', recipients=['ashley_e_chang@brown.edu'])
    msg.html = render_template("PersonalMessageEmailTemplate/Code/index.html", name=name,
                               email=email, subject=subject, message=message)
    mail.send(msg)
    return "Sent"


def send_personal_email(email, subject, name, message):
    msg = Message(subject, sender='ursaminorsweb@gmail.com', recipients=['ashley_e_chang@brown.edu'])
    msg.html = render_template("PersonalMessageEmailTemplate/Code/index.html", name=name,
                               email=email, subject=subject,
                               message=Markup("Personal Website Contact Form Response: <br>" + message))
    mail.send(msg)
    return "Sent"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ursaminorsweb@gmail.com'
app.config['MAIL_PASSWORD'] = 'hiygxhofxbpcabxq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
guard.init_app(app, User)

with app.app_context():
    if db.session.query(User).filter_by(username='spswatron').count() < 1:
        db.session.add(User(
          username='spswatron',
          password=guard.hash_password('b7f78a19708cb3556faa6c51e0d03f2eacb13e92'),
          roles='admin'
        ))
    else:
        users = db.session.query(User).all()
        me =list(filter(lambda x: x.username == 'spswatron', users))[0]
        me.password = guard.hash_password('b7f78a19708cb3556faa6c51e0d03f2eacb13e92')

    db.session.commit()


@app.route('/', methods=["GET", "POST"])
def all_responses():
    return redirect("https://www.ashley-chang.me/index")


@app.route('/alumni', methods=["GET", "POST"])
def alumni():
    if request.method == "POST":
        client = gspread.authorize(credential)
        alumni = client.open("Alumni Bios").sheet1
        return jsonify(alumni.get_all_records())


@app.route('/members', methods=["GET", "POST"])
def members():
    if request.method == "POST":
        client = gspread.authorize(credential)
        current_members = client.open("Current Member Bios").sheet1
        return jsonify(current_members.get_all_records())


@app.route('/update_db', methods=["GET", "POST"])
def update_db():
    return "a"


@app.route('/submit_form', methods=["POST"])
def submit_form():
    print(request)
    if request.method == 'POST':
        response = request.get_json()
        send_email(response['email'], "Ursas Website Contact", response['name'], response['message'])
        return 'Sent'
    return "Not Post"


@app.route('/submit_personal_form', methods=["POST"])
def submit_personal_form():
    print(request)
    if request.method == 'POST':
        response = request.get_json()
        send_personal_email(response['email'], response['subject'], response['name'], response['message'])
        return 'Sent'
    return "Not Post"


@app.route("/send_mail", methods=['GET', 'POST'])
def index():
    return "Sent"


@app.route("/random_genre", methods=['GET', 'POST'])
def r_genre():
    return random_genre()


<<<<<<< HEAD
if __name__ == '__main__':
   app.run(host='0.0.0.0')
=======
def doc_to_html_message(response, soup):
    msg = Message("file upload", sender='ursaminorsweb@gmail.com', recipients=['spswatron@gmail.com'])
    response.save(response.filename)
    with app.open_resource(response.filename) as fp:
        msg.attach(response.filename, response.content_type, fp.read())
    html_name = response.filename.split('.')[0] + '.txt'
    msg.attach(response.filename, response.content_type, fp.read())
    msg.attach(html_name, 'text/txt', soup.prettify())
    mail.send(msg)
    os.remove(response.filename)
>>>>>>> 2961b47bc78a31774d9e551f79f77f13b927ad0c


from blog import *


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
