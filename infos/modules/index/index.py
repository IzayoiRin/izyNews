from flask import json

from infos.models import Users
from infos.modules import response_code as rc


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


indexlog = IndexLogical()
