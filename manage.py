import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import User, Post
import sqlalchemy_utils
from __init__ import app, db

with app.app_context():
    db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()

app.config.from_object(os.environ['APP_SETTINGS'])
app.app_context().push()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()