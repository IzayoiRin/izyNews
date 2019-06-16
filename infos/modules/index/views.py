from flask import session, render_template, current_app, send_file, request

from . import indexBlp
from .index import IndexLogical


@indexBlp.route('/', methods=['GET', 'POST'])
def index():
    indexlog = IndexLogical()
    context = indexlog.main_scoop()
    return render_template("news/index.html", data=context)


@indexBlp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file("news/favicon.ico")
    # return send_file("/infos/static/news/favicon.ico")
    # redirect


@indexBlp.route('/login_state', methods=("GET",))
def login_state():
    indexlog = IndexLogical()
    indexlog.requset = session.get("uid", None)
    indexlog.login_state()
    return indexlog.response


@indexBlp.route("/hot_rank", methods=("GET",))
def hot_rank():
    indexlog = IndexLogical()
    indexlog.requset = None
    indexlog.hot_rank()
    return indexlog.response

