#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify
)
from .forms import LoginForm, ResetpwdForm, ResetEmailForm, AddbannerForm, UpdateBanner, AddbordsForm, UboardsForm
from .models import CMSUser, CMSPermissions
from .decorators import login_need, permissions_need
import config
from exit import db, mail
from flask_mail import Message
from utils import restful, clcache
import string, random
from ..models import Banner
from ..common.models import Boards, PostModel, Essence_post, CommentsModel
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route('/')
@login_need
def index():
    return render_template('cms/cms_index.html')


@bp.route('/login_out/')
@login_need
def login_out():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/banners/')
@login_need
def banners():
    banners = Banner.query.order_by(Banner.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/addbanner/', methods=['POST'])
@login_need
def addbanner():
    form = AddbannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        user = Banner(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(user)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/', methods=['POST'])
@login_need
def ubanner():
    form = UpdateBanner(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = Banner.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=u'没有这个轮播图')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message=u'请输入banner_id')
    banner = Banner.query.get(banner_id)
    if not banner:
        return restful.params_error(message=u'没有这个轮播图')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error(u'请传递正确的邮箱')

    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 6))

    message = Message("BBS论坛验证码", recipients=[email], body=u'您的验证码是：%s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    clcache.set(email, captcha)
    return restful.success()


@bp.route('/profile/')
@login_need
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/posts/')
@login_need
@permissions_need(CMSPermissions.poster)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * 10
    end = start + 10
    post = PostModel.query.order_by(PostModel.create_time.desc()).slice(start, end)
    total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total)
    return render_template('cms/cms_posts.html', posts=post, pagination=pagination)


@bp.route('/dpost/', methods=['POST'])
@login_need
@permissions_need(CMSPermissions.poster)
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请输入帖子ID')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message='没有这篇帖子')
    db.session.delete(post)
    db.session.commit()
    return restful.success()


@bp.route('/epost/', methods=['POST'])
@login_need
@permissions_need(CMSPermissions.poster)
def essence_post():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请输入这篇帖子的id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子')
    essence = Essence_post()
    essence.post = post
    db.session.add(essence)
    db.session.commit()
    return restful.success()


@bp.route('/uepost/', methods=['POST'])
@login_need
@permissions_need(CMSPermissions.poster)
def ue_post():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请输入人这篇帖子的id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子')
    essence = Essence_post.query.filter_by(post_id=post_id).first()
    db.session.delete(essence)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_need
@permissions_need(CMSPermissions.commenter)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_need
@permissions_need(CMSPermissions.boarder)
def boards():
    board_model = Boards.query.all()
    context = {
        'boards': board_model
    }
    return render_template('cms/cms_boards.html', **context)


@bp.route('/aboards/', methods=['POST'])
@login_need
@permissions_need(CMSPermissions.boarder)
def aboards():
    form = AddbordsForm(request.form)
    if form.validate():
        name = form.name.data
        board = Boards(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uboards/', methods=['POST'])
@login_need
@permissions_need(CMSPermissions.boarder)
def uboards():
    form = UboardsForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = Boards.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboards/', methods=['POST'])
@login_need
@permissions_need(CMSPermissions.boarder)
def dboards():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error(message='没有这个板块ID')

    board = Boards.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块')

    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/fusers/')
@login_need
@permissions_need(CMSPermissions.frontuser)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_need
@permissions_need(CMSPermissions.cmsuser)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_need
@permissions_need(CMSPermissions.all_permisssions)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/resetpwd/', methods=['GET', 'POST'])
@login_need
def resetpwd():
    if request.method == 'GET':
        return render_template('cms/cms_resetpwd.html')
    else:
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                # return jsonify({"code":400,"message":"旧密码输入错误"})
                return restful.params_error("旧密码错误")
        else:
            return restful.params_error(form.get_error())


@bp.route('/resetemail/', methods=['GET', 'POST'])
@login_need
def resetemail():
    if request.method == 'GET':
        return render_template('cms/cms_resetemail.html')
    else:
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('cms/cms_login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True

                return redirect(url_for('cms.index'))
            else:
                message = '邮箱或者密码输入错误'
                return render_template('cms/cms_login.html', message=message)
        else:
            message = form.get_error()
            return render_template('cms/cms_login.html', message=message)
