import logging

from flask import json
from infos.models import Users, News
from infos.modules import response_code as rc
from infos import constants as ct


class IndexLogical(object):

    def __init__(self):
        self.requset = None
        self.response = None

    def login_state(self):
        uid = self.requset
        if not uid:
            self.response = json.jsonify(errno=rc.RET.SESSIONERR, errmsg="Session Invalid")
        user = Users.packQuery(Users.id == uid)
        select_user = user[0] if user else None
        if select_user:
            self.response = json.jsonify(errno=rc.RET.OK, name=select_user.nick_name, url=select_user.avatar_url)
            return
        self.response = json.jsonify(errno=rc.RET.USERERR, errmsg="Error User")

    def hot_rank(self, *criterion):
        filters = [News.is_delete == 0] + list(criterion)
        try:
            queries = News.query.filter(*filters).order_by(News.hot.desc()).limit(ct.CLICK_RANK_MAX_NEWS).all()
        except Exception as e:
            logging.error(e)
            self.response = json.jsonify(errno=rc.RET.DBERR, errmsg="Query failed")
            return
        tops = [query.packDict("title", "id") for query in queries]
        self.response = json.dumps(tops)
