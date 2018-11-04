#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flask import session,g
from .views import bp
import config
from .models import CMSUser,CMSPermissions


@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user



@bp.context_processor
def context_processor():
    return {'CMSPermissions':CMSPermissions}