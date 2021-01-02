from flask_mail import Message
from random_genre import random_genre
from flask import *
import gspread
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
from flask import Flask
from os.path import join, dirname, realpath
from oauth2client.service_account import ServiceAccountCredentials
from dial_sherlock import call_sherlock
import pytesseract
import numpy
import cv2
from pdf2image import convert_from_bytes
import tempfile
from flask_socketio import SocketIO, emit
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


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
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["400 per day", "70 per hour"]
)


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


def send_email_ocr(filename, recipient, message):
    msg = Message("OCR results | " + filename.replace(".txt", ""), sender='ursaminorsweb@gmail.com', recipients=[recipient],
                  body=Markup(message))
    msg.attach(filename, "text/plain", message)
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


@app.route('/send_ocr_email', methods=["POST"])
def send_ocr_email():
    response = request.get_json()
    a = request
    return send_email_ocr(response['filename'], response['recipient'], response['message'])


@limiter.exempt
@app.route("/random_genre", methods=['GET', 'POST'])
def r_genre():
    return random_genre()


@socketio.on('sherlock')
def sherlock(username):
    results = call_sherlock(username)
    emit("sherlock", {"end": "end"})


def process_image(npimg, languages, image: bool):
    img = None
    if image:
        img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    else:
        img = cv2.imread(npimg)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    languages = '+'.join(languages)
    result = pytesseract.image_to_string(img, config=r'--oem 3 --psm 4', lang=languages)
    return result


@socketio.on('ocr_upload')
def ocr_upload(formData):
    emit("ocr_upload", {"stats": [1, 50]})
    filestr = formData['file']
    # convert string data to numpy array
    npimg = numpy.fromstring(filestr, numpy.uint8)
    languages = formData['languages']
    result = ""
    if '.pdf' in formData['filename']:
        with tempfile.TemporaryDirectory() as path:
            images = convert_from_bytes(npimg, output_folder=path)
            i = 1
            emit("ocr_upload", {"stats": [i / 2, len(images)]})
            for image in images:
                print(image.filename)
                result += process_image(image.filename, languages, False)
                emit("ocr_upload", {"stats": [i, len(images)]})
                i += 1

    else:
        result = process_image(npimg, languages, True)

    d = "\n"
    result = ''.join(["<p>" + e + "</p>" for e in result.split(d) if e])

    emit("ocr_upload", {"ocr": result})


if __name__ == '__main__':
    socketio.run(debug=True, host='0.0.0.0')
