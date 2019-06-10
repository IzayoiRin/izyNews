import logging
import re
from random import randint
from flask import make_response, abort, jsonify
from infos.modules import constants as ct, response_code as rc
from Activation import factory
from infos.utils.captcha import captcha as cap
from infos.libs.yuntongxun import sms


class PassPort(object):

    ccp = sms.CCP()
    redis_db = factory("redis")

    def __init__(self):
        self.request = None
        self.rds_query = None  # type: str
        self.response = None

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
            return jsonify(errno=rc.RET.DATAERR, errmsg="WRONG IMAGE CODE")

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


ps_port = PassPort()
