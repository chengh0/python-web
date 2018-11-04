#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flask import jsonify

class HttpCode():
    ok = 200
    unautherror = 400
    paramserror = 401
    servererror = 500

def restful_result(code,message,data):
    return jsonify({"code":code,"message":message,"data":data})

def success(message="",data=None):
    return restful_result(code=HttpCode.ok,message=message,data=data)

def unauth_error(message=""):
    return restful_result(code=HttpCode.unautherror,message=message,data=None)

def params_error(message=""):
    return restful_result(code=HttpCode.paramserror,message=message,data=None)

def server_error(message=""):
    return restful_result(code=HttpCode.servererror,message=message or '服务器内部错误',data=None)