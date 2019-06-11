from flask import session, render_template, current_app, send_file
from . import indexBlp


@indexBlp.route('/', methods=['GET', 'POST'])
def index():
    # set session and saving to redis though flask_session
    uid = session.get("uid", None)
    print(uid)
    return render_template("news/index.html")


@indexBlp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file("news/favicon.ico")
    # return send_file("/infos/static/news/favicon.ico")
    # redirect
