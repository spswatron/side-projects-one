from flask import *
from app import *
from models import User, Post
import flask_praetorian
from bs4 import BeautifulSoup as bs
import mammoth
import string


def convert_title(title):
    return title.translate(str.maketrans('', '', string.punctuation))\
        .replace(" ", "_").replace("'", "").replace('"', "").lower()


@app.route("/all_posts", methods=['GET', 'POST'])
@flask_praetorian.auth_required
def all_posts():
    posts = db.session.query(Post).all()
    posts = sorted(list(map(lambda s: s.json(), posts)), key=lambda s: s['id'], reverse=True)
    return {'posts': posts}


@app.route('/cms/login', methods=['POST'])
def cms_login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    """
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200


@app.route('/cms/auth_check', methods=['GET'])
@flask_praetorian.auth_required
def auth_check():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    """
    return {'result': 'success'}


@app.route('/cms/refresh', methods=['POST'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200


@app.route("/all_show_posts", methods=['GET', 'POST'])
def all_show_posts():
    posts = db.session.query(Post).all()
    posts = sorted(list(map(lambda s: s.json(), posts)), key=lambda s: s['id'], reverse=True)
    posts = list(filter(lambda s: s['show'], posts))
    return {'posts': posts}


def post_list():
    posts = db.session.query(Post).all()
    posts = sorted(list(map(lambda s: s.json(), posts)), key=lambda s: s['id'], reverse=True)
    return posts


@app.route("/delete_post/<number>", methods=['POST', 'DELETE'])
@flask_praetorian.auth_required
def delete_post(number):
    if request.method == 'POST':
        Post.query.get(number).show = not Post.query.get(number).show
        db.session.commit()
        return {'posts': post_list()}

    elif request.method == 'DELETE':
        Post.query.filter_by(id=number).delete()
        db.session.commit()
        return {'posts': post_list()}


@app.route("/get_post/<url>", methods=['POST', 'DELETE'])
def get_post(url):
    if request.method == 'POST':
        posts = db.session.query(Post).all()
        posts = list(filter(lambda x: x.url.lower() == url.lower() and x.show, posts))
        if len(posts) > 0:
            return posts[0].json()
        else:
            return {}


@app.route("/get_demo_post/<url>", methods=['POST', 'DELETE'])
@flask_praetorian.auth_required
def get_demo_post(url):
    if request.method == 'POST':
        posts = db.session.query(Post).all()
        posts = list(filter(lambda x: x.url.lower() == url.lower(), posts))
        if len(posts) > 0:
            return posts[0].json()
        else:
            return {}


@app.route("/modify_post/<number>", methods=['POST', 'DELETE'])
@flask_praetorian.auth_required
def modify_post(number):
    if request.method == 'POST':
        to_change = Post.query.get(number)
        to_change.content = request.json['content']
        to_change.title = request.json['title']
        to_change.url = convert_title(to_change.title)
        db.session.commit()
        return to_change.json()


@app.route("/html_new_post", methods=['POST'])
@flask_praetorian.auth_required
def html_new_post():
    if request.method == 'POST':
        title = request.json['title']
        url = convert_title(title)
        same_url = list(filter(lambda y: y.url == convert_title(title),
                                 db.session.query(Post).all()))
        html = request.json['html']
        if len(same_url) == 0:
            new_post = Post(url=url, title=title, content=html)
            new_post.save()
            return {'html': html,
                    'id': new_post.id,
                    'posts': post_list()}
        raise InvalidUsage('A post with this title already exists. Try another one?', status_code=410)


@app.route("/doc_to_html", methods=['GET', 'POST'])
@flask_praetorian.auth_required
def doc_to_pdf():
    if request.method == 'POST':
        response = request.files['myFile']
        result = mammoth.convert_to_html(response)
        html = bs(result.value, 'html.parser').prettify()
        title = response.filename.split(".")[0]
        url = convert_title(title)
        same_url = list(filter(lambda x: x.url == convert_title(title),
                                 db.session.query(Post).all()))
        if len(same_url) == 0:
            new_post = Post(url=url, title=title, content=html)
            new_post.save()
            return_post = new_post
        else:
            same_url[0].content = html
            db.session.commit()
            return_post = same_url[0]

        return {'html': html,
                'id': return_post.id,
                'posts': post_list()}
