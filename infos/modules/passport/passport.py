import re
from random import randint
from flask import make_response, abort, jsonify, session
from infos import REDIS
from infos import constants as ct
from infos.libs.yuntongxun import sms
from infos.models import *
from infos.modules import response_code as rc
from infos.utils.captcha import captcha as cap
from infos.utils.common import BaseModules


class PassPort(BaseModules):

    ccp = sms.CCP()
    redis_db = REDIS

    def __init__(self):
        super().__init__()
        self.rds_query = None  # type: str

    def img_code(self):
        # resolute request
        # request verification
        if not self.request:
            abort(404)
        # main function: create img code
        _, code, img = cap.captcha.generate_captcha()
        print(111111111111111111111, code)
        self._redis_operate(name="imgCode:" + self.request, time=ct.IMAGE_CODE_REDIS_EXPIRES, value=code)
        self.response = make_response(img, 200, {"Content-Type": "image/jpg"})

    def sms_code(self):
        # resolute request
        mobile, img, uuid = self.request.get("mobile"), self.request.get("img"), self.request.get("uuid")
        # request verification
        flag = self._request_verify(mobile, img, "imgCode:" + uuid)

        if flag:
            self.response = flag
            return
        # main function: set sms code
        sms = "%06d" % randint(0, 999999)
        timeout = ct.SMS_CODE_REDIS_EXPIRES
        # if self.ccp.send_template_sms('18516952650', [sms, timeout], 1) < 0:
        #     self.response = jsonify(errno=rc.RET.THIRDERR, errmsg="SMS Sent Fail")
        #     return
        print(111111111111111111111, sms)
        self._redis_operate(name="mobile:" + mobile, time=timeout, value=sms)
        self.response = jsonify(errno=rc.RET.OK)

    def register(self):
        # resolute request
        mobile, smscode, password = self.request.get("mobile"),self.request.get("smscode"),self.request.get("password")
        # request verification
        flag = self._request_verify(mobile, smscode, "mobile:"+mobile)
        if flag:
            self.response = flag
            return
        # main function: add a raw to db.users
        new_user = Users()
        try:
            new_user.encode_pwd = password
            new_user.add_raw(mobile=mobile, nick_name=mobile, last_login=datetime.now())
        except DatabaseError as e:
            self.response = jsonify(errno=rc.RET.DBERR, errmsg=str(e))
            return
        except Exception as e:
            logging.error(e)
            self.response = jsonify(errno=rc.RET.UNKOWNERR, errmsg="AN UNKNOWN ERROR")
            return
        session["uid"] = new_user.id
        self.response = jsonify(errno=rc.RET.OK)

    def login(self):
        mobile, password = self.request.get("mobile"), self.request.get("passport")
        if not(mobile and password):
            return jsonify(errno=rc.RET.PARAMERR, errmsg="LOST PARAMS")
        user = Users.packQuery(Users.mobile == mobile)
        flag = (user[0].id if user[0].verify_pwd(password) else None) if user else None
        if flag is None:
            self.response = jsonify(errno=rc.RET.USERERR, errmsg="MOBILE OR PASSWORD WRONG")
            return
        session["uid"] = flag
        self.response = jsonify(errno=rc.RET.OK)

    def logout(self):
        if self.request.pop("uid", None):
            self.response = '1'
            return
        self.response = '0'

    def _request_verify(self,*args):
        """
        Verification params: mobile, req_dat, query_key
        :param moblie: client's phone number
        :param req_dat: client's verified request data
        :param query_key: server's verified redis key
        :return None: repr Verified
        :return Others: json response [errno, errmsg]
        """
        if not all(args):
            return jsonify(errno=rc.RET.PARAMERR, errmsg="LOST PARAMS")
        mobile, req_dat, query_key = args
        if re.match(r"^1[35678]\d{9}$", mobile) is None:
            return jsonify(errno=rc.RET.USERERR, errmsg="ILLEGAL PHONE NUMBER")
        self._redis_operate(query_key)
        if self.rds_query.upper() != req_dat.upper() if self.rds_query else 1:
            return jsonify(errno=rc.RET.DATAERR, errmsg="WRONG VERIFY CODE")
        # mobile's unique verification
        try:
            if Users.query.filter_by(mobile=mobile).first():
                return jsonify(errno=rc.RET.DATAEXIST, errmsg="THE MOBILE HAS BEEN REGISTERED")
        except Exception as e:
            logging.error(e)
            return jsonify(errno=rc.RET.UNKOWNERR, errmsg="AN UNKNOWN ERROR")

    def _redis_operate(self, *args, **kwargs):
        if args:
            try:
                self.rds_query = self.redis_db.get(args[0])
            except Exception as e:
                logging.error(e)
                abort(500)
        elif kwargs:
            try:
                self.rds_query = self.redis_db.setex(**kwargs)
            except Exception as e:
                logging.error(e)
                abort(500)
