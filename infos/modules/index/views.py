from flask import session, render_template, current_app, send_file
from . import indexBlp
from .index import indexlog


@indexBlp.route('/', methods=['GET', 'POST'])
def index():
    # set session and saving to redis though flask_session
    return render_template("news/index.html")


@indexBlp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file("news/favicon.ico")
    # return send_file("/infos/static/news/favicon.ico")
    # redirect


@indexBlp.route('/login_state', methods=("GET",))
def login_state():
    indexlog.requset = session.get("uid", None)
    indexlog.login_state()
    return indexlog.response
