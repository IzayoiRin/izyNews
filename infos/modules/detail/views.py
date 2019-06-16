from flask import session, render_template, current_app, send_file, request
from . import detailBlp
from .detail import Detail


@detailBlp.route('/<int:news_id>')
def index(news_id):
    dtl = Detail()
    dtl.request = news_id
    context = dtl.main_content()
    if context:
        return render_template('news/detail.html', data=context)
    return dtl.response
