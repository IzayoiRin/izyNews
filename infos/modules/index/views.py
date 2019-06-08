from flask import session, render_template, current_app, send_file
from . import indexBlp
from Activation import factory

redis_db = factory("redis")


@indexBlp.route('/', methods=['GET', 'POST'])
def index():
    # set session and saving to redis though flask_session
    session["asd"] = 123
    # redis_db.set('asd', 123)
    return render_template("news/index.html")


@indexBlp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file("news/favicon.ico")
    # TODO return send_file("/infos/static/news/favicon.ico")
    # TODO redirect