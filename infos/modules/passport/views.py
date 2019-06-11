from flask import request
from . import passportBlp
from .passport import ps_port


@passportBlp.route("/imageCode")
def get_image_code():
    """API:
    request_type: GET
    recv_data: /imageCode?imageCode= [UUID]
    sent_data: image/jpg
    """
    ps_port.request = request.args.get("imageCode")
    ps_port.img_code()
    return ps_port.response


@passportBlp.route("/smsCode", methods=("POST",))
def sms_code():
    """
    API:
    request_type: POST
    recv_data: json / {"mobile": [], "img": [],"uuid": []}
    sent_data: json / {"errno": [], "errmsg": []}
    """
    ps_port.request = request.json
    ps_port.sms_code()
    return ps_port.response


@passportBlp.route("/register", methods=("POST",))
def register():
    ps_port.request = request.json
    ps_port.register()
    return ps_port.response


@passportBlp.route("/login", methods=("POST",))
def login():
    ps_port.request = request.json
    ps_port.login()
    return ps_port.response
