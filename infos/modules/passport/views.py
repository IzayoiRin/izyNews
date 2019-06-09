from flask import request
from . import passportBlp
from .passport import ps_port


@passportBlp.route("/imageCode")
def get_image_code():
    ps_port.request = request.args.get("imageCode")
    ps_port.img_code()
    return ps_port.response


@passportBlp.route("/smsCode", methods=("POST",))
def sms_code():
    ps_port.request = request.json
    ps_port.sms_code()
    return ps_port.response
