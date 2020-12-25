from flask_mail import Message
from random_genre import random_genre
from flask import *
import gspread
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
from flask import Flask
from os.path import join, dirname, realpath
from oauth2client.service_account import ServiceAccountCredentials
from sherlock.dial_sherlock import dial_sherlock


app = Flask(__name__)
credential = ServiceAccountCredentials.from_json_keyfile_name(join(dirname(realpath(__file__)), 'ursas.json'),
                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",
                                                               "https://www.googleapis.com/auth/drive"])
cors = CORS(app, resources={r'/*': {"origins": '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ursaminorsweb@gmail.com'
app.config['MAIL_PASSWORD'] = 'hiygxhofxbpcabxq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


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


@app.route('/', methods=["GET", "POST"])
def all_responses():
    return "wecome to api"


@app.route('/alumni', methods=["GET", "POST"])
def alumni():
    if request.method == "POST":
        client = gspread.authorize(credential)
        alumni_list = client.open("Alumni Bios").sheet1
        return jsonify(alumni_list.get_all_records())


@app.route('/members', methods=["GET", "POST"])
def members():
    if request.method == "POST":
        client = gspread.authorize(credential)
        current_members = client.open("Current Member Bios").sheet1
        return jsonify(current_members.get_all_records())


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


@app.route("/sherlock/<username>", methods=['GET', 'POST'])
def sherlock(username):
    results = dial_sherlock(username)
    for pair in results:
        for key in pair:
            pair[key] = pair[key].replace("\\n', ", "").replace("\\n']", "")
    return {"matches": results}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
