#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flask import session,redirect,url_for,g
from functools import wraps
import config


def login_need(func):
    @wraps(func)
    def need(*args,**kwargs):
        if config.CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return need


def permissions_need(permission):
    def outter(func):
        @wraps(func)
        def need(*args,**kwargs):
            user = g.cms_user
            if user.has_permissions(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for('cms.index'))
        return need
    return outter