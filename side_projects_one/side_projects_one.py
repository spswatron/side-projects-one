from flask_mail import Message
from random_genre import random_genre
from flask import jsonify, render_template, request, redirect, Markup, Blueprint
from __init__ import app, mail, credential
import gspread

side_project_one = Blueprint('blog', __name__, template_folder='templates')


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


@side_project_one.route('/', methods=["GET", "POST"])
def all_responses():
    return redirect("https://www.ashley-chang.me/index")


@side_project_one.route('/alumni', methods=["GET", "POST"])
def alumni():
    if request.method == "POST":
        client = gspread.authorize(credential)
        alumni = client.open("Alumni Bios").sheet1
        return jsonify(alumni.get_all_records())


@side_project_one.route('/members', methods=["GET", "POST"])
def members():
    if request.method == "POST":
        client = gspread.authorize(credential)
        current_members = client.open("Current Member Bios").sheet1
        return jsonify(current_members.get_all_records())


@side_project_one.route('/submit_form', methods=["POST"])
def submit_form():
    print(request)
    if request.method == 'POST':
        response = request.get_json()
        send_email(response['email'], "Ursas Website Contact", response['name'], response['message'])
        return 'Sent'
    return "Not Post"


@side_project_one.route('/submit_personal_form', methods=["POST"])
def submit_personal_form():
    print(request)
    if request.method == 'POST':
        response = request.get_json()
        send_personal_email(response['email'], response['subject'], response['name'], response['message'])
        return 'Sent'
    return "Not Post"


@side_project_one.route("/send_mail", methods=['GET', 'POST'])
def index():
    return "Sent"


@side_project_one.route("/random_genre", methods=['GET', 'POST'])
def r_genre():
    return random_genre()
