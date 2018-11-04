#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flask import Blueprint
from utils.captcha import Captcha
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    make_response,
    session,
    url_for,
)

from utils import clcache
from io import BytesIO
from utils import restful,safeutils
from exit import db
import config
from ..models import Banner

bp = Blueprint("common",__name__,url_prefix="/common")


@bp.route('/')
def index():
    return 'common index'


@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    captcha = request.args.get('graph_captcha')
    if captcha:
        clcache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    captcha = request.form.get('graph_captcha')
    return resp