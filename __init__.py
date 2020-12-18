from flask import *
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os.path import join, dirname, realpath
from oauth2client.service_account import ServiceAccountCredentials
from flask_moment import Moment
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

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ursaminorsweb@gmail.com'
app.config['MAIL_PASSWORD'] = 'hiygxhofxbpcabxq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
guard = flask_praetorian.Praetorian()


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
