from flask import session, render_template, current_app, send_file, request

from . import indexBlp
from .index import IndexLogical


@indexBlp.route('/', methods=['GET', 'POST'])
def index():
    indexlog = IndexLogical()
    context = indexlog.main_categroy()
    return render_template("news/index.html", data=context)


@indexBlp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file("news/favicon.ico")
    # return send_file("/infos/static/news/favicon.ico")
    # redirect


@indexBlp.route('/news_list', methods=("GET",))
def news_list():
    indexlog = IndexLogical()
    indexlog.request = request.args
    indexlog.main_news()
    return indexlog.response


@indexBlp.route('/login_state', methods=("GET",))
def login_state():
    indexlog = IndexLogical()
    indexlog.request = session.get("uid", None)
    indexlog.login_state()
    return indexlog.response


@indexBlp.route("/hot_rank", methods=("GET",))
def hot_rank():
    indexlog = IndexLogical()
    indexlog.request = None
    indexlog.hot_rank()
    return indexlog.response

