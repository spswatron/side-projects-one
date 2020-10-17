from flask import Flask, request, url_for, jsonify
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
from os.path import join, dirname, realpath
import gspread
from oauth2client.service_account import ServiceAccountCredentials

credential = ServiceAccountCredentials.from_json_keyfile_name(join(dirname(realpath(__file__)), 'ursas.json'),
                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",
                                                               "https://www.googleapis.com/auth/drive"])

app = Flask(__name__)
CORS(app)
mail= Mail(app)


def send_email():
    msg = Message('Hello', sender='ursaminorsweb@gmail.com', recipients=['ashley_e_chang@brown.edu'])
    msg.body = "Hi there good job for figuring out how this technology works"
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
    client = gspread.authorize(credential)
    alumni = client.open("Alumni Bios").sheet1
    if request.method == "POST":
        return jsonify(alumni.get_all_records())
    else:
        return "Huh"


@app.route('/members', methods=["GET", "POST"])
def members():
    client = gspread.authorize(credential)
    current_members = client.open("Current Member Bios").sheet1
    if request.method == "POST":
        return jsonify(current_members.get_all_records())
    else:
        return "Huh"



@app.route('/submit_form', methods=["POST"])
def submit_form():
    print('lsdfdkafdf')
    print(request)
    if request.method == 'POST':
        msg = Message('Hello', sender='ursaminorsweb@gmail.com', recipients=['ashley_e_chang@brown.edu'])
        response = request.get_json()
        msg.body = 'name: ' + response['name'] + '\n' + \
                   'email: ' + response['email'] + '\n' + \
                   'message: ' + response['message']
        mail.send(msg)
        return 'Sent'
    return "Not Post"


@app.route("/send_mail", methods=['GET', 'POST'])
def index():
    send_email()
    return "Sent"


if __name__ == '__main__':
   app.run(debug = True)