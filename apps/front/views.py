#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    make_response,
    session,
    url_for,
    g,
    abort,
    redirect
)

from utils import clcache
from io import BytesIO
from .forms import SignupForm,LoginForm,AddPost,AddCommentsForm
from utils import restful,safeutils
from .models import FrontUser
from apps.cms.models import CMSPermissions
from exit import db
import config
from ..models import Banner
from ..common.models import Boards,PostModel,CommentsModel,Essence_post
from .decorators import login_need,permissions_need
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy.sql import func



bp = Blueprint("front",__name__)


@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get('st',type=int,default=1)
    banners = Banner.query.order_by(Banner.priority.desc()).limit(4)
    borads = Boards.query.all()
    start = (page-1) * config.PER_PAGE
    end = start + config.PER_PAGE
    posts = None
    total = 0
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        query_obj = db.session.query(PostModel).outerjoin(Essence_post).order_by(Essence_post.create_time.desc(),PostModel.create_time.desc())
    elif sort == 3:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        query_obj = db.session.query(PostModel).outerjoin(CommentsModel).group_by(PostModel.id).order_by(func.count(CommentsModel.id).desc(),PostModel.create_time.desc())



    if board_id:
        posts = query_obj.filter(PostModel.board_id==board_id).slice(start,end)
        total = query_obj.filter(PostModel.board_id==board_id).count()
    else:
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total)
    context = {
        'banners':banners,
        'boards':borads,
        'posts':posts,
        'pagination':pagination,
        'board_id':board_id,
        'corrent_sort':sort
    }
    return render_template('front/front_index.html',**context)


@bp.route('/apost/',methods=['GET','POST'])
@login_need
def apost():
    if request.method == 'GET':
        boards = Boards.query.all()
        context = {
            'boards':boards
        }
        return render_template('front/front_apost.html',**context)
    else:
        form = AddPost(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = Boards.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块')
            post = PostModel(title=title,content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


@bp.route('/post/<post_id>/')
def post_details(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_post_details.html',post=post)


@bp.route('/acomments/',methods=['POST'])
@login_need
def add_comments():
    form = AddCommentsForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentsModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这篇帖子')
    else:
        return restful.params_error(form.get_error())


@bp.route('/login_out/')
@login_need
def login_out():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('front.login'))




class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html',return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())


class LoginView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup'):
            return render_template('front/front_login.html', return_to=return_to)
        else:
            return render_template('front/front_login.html')
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter(FrontUser.telephone==telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机号码或者密码输入错误')
        else:
            return restful.params_error(message=form.get_error())



bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))