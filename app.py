from __init__ import guard, mail, app, db
from models import User
from blog.blog import blog
from side_projects_one.side_projects_one import side_project_one

app.register_blueprint(blog)
app.register_blueprint(side_project_one)
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
        me = list(filter(lambda x: x.username == 'spswatron', users))[0]
        me.password = guard.hash_password('b7f78a19708cb3556faa6c51e0d03f2eacb13e92')

    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
