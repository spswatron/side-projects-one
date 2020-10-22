from flask import *
from flask_cors import CORS
from flask_mail import Mail, Message
from flask import Flask
from os.path import join, dirname, realpath
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dataclasses import dataclass


credential = ServiceAccountCredentials.from_json_keyfile_name(join(dirname(realpath(__file__)), 'ursas.json'),
                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",
                                                             "https://www.googleapis.com/auth/drive"])

app = Flask(__name__)
CORS(app)
mail= Mail(app)


#database names: alumni, current_members

@dataclass
class Email:
    """Class for keeping track of details for email."""
    header: str
    name: str
    e_address: str
    subject: str
    message: str

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


def send_email(email, subject, name, message):
    msg = Message(subject, sender='ursaminorsweb@gmail.com', recipients=['ashley_e_chang@brown.edu'])
    msg.html = render_template("PersonalMessageEmailTemplate/Code/index.html", name=name,
                               email=email, subject = subject, message = message)
    mail.send(msg)
    return "Sent"


def send_personal_email(email, subject, name, message):
    msg = Message(subject, sender='ursaminorsweb@gmail.com', recipients=['ashley_e_chang@brown.edu'])
    msg.html = render_template("PersonalMessageEmailTemplate/Code/index.html", name=name,
                               email = email, subject = subject, message = "Personal Website Contact Form Response \n" + message)
    mail.send(msg)
    return "Sent"


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ursaminorsweb@gmail.com'
app.config['MAIL_PASSWORD'] = 'hiygxhofxbpcabxq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/', methods=["GET", "POST"])
def all_responses():
    return "Huh"


@app.route('/alumni', methods=["GET", "POST"])
def alumni():
    if request.method == "POST":
        client = gspread.authorize(credential)
        alumni = client.open("Alumni Bios").sheet1
        return jsonify(alumni.get_all_records())
    else:
        return "Huh"


@app.route('/members', methods=["GET", "POST"])
def members():
    if request.method == "POST":
        client = gspread.authorize(credential)
        current_members = client.open("Current Member Bios").sheet1
        return jsonify(current_members.get_all_records())
    else:
        return "Huh"


@app.route('/update_db', methods=["GET", "POST"])
def update_db():
    return "a"


@app.route('/submit_form', methods=["POST"])
def submit_form():
    print('lsdfdkafdf')
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
    send_email("ashley_e_chang@brown.edu", "tester", "Ashley", "this is the message. have fun buddy.")
    return "Sent"


if __name__ == '__main__':
   app.run(debug = True)