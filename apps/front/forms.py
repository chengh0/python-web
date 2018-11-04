#!/usr/bin/python
#  -*- coding: utf-8 -*-
from ..forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp,Length,EqualTo,ValidationError,InputRequired
from utils import clcache



# class SignupForm(BaseForm):
# #     telephone = StringField(validators=[Regexp(r"1[34578]\d{9}",message='请输入正确格式的手机号码')])
# #     username = StringField(validators=[Length(2,20,message='请输入正确格式的用户名')])
# #     password = StringField(validators=[Length(4,20,message='请输入正确格式的密码')])
# #     password2 = StringField(validators=[EqualTo('password',message='两次密码输入不相同')])
# #     graph_captcha = StringField(validators=[Regexp(r"\w{4}", message='请输入正确格式的验证码！')])
# #
# #
# #     def validate_graph_captcha(self,field):
# #         graph_captcha = field.data
# #         graph_captcha_mem = clcache.get(graph_captcha.lower())
# #
# #         if not graph_captcha_mem:
# #             raise ValidationError(message='验证码输入错误！')
#encoding: utf-8

from ..forms import BaseForm
from wtforms import StringField
from wtforms.validators import Regexp,EqualTo,ValidationError
from utils import clcache

class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}",message='请输入正确格式的手机号码！')])
    username = StringField(validators=[Regexp(r".{2,20}",message='请输入正确格式的用户名！')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}",message='请输入正确格式的密码！')])
    password2 = StringField(validators=[EqualTo("password1",message='两次输入的密码不一致！')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}",message='请输入正确格式的验证码！')])



    def validate_graph_captcha(self,field):
        graph_captcha = field.data

        graph_captcha_mem = clcache.get(graph_captcha.lower())
        if not graph_captcha_mem:
            raise ValidationError(message='图形验证码错误！')



class LoginForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[34578]\d{9}", message='请输入正确格式的手机号码')])
    password = StringField(validators=[Length(4, 20, message='请输入正确格式的密码')])
    remember = StringField()


class AddPost(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题')])
    content = StringField(validators=[InputRequired(message='请输入内容')])
    board_id = IntegerField(validators=[InputRequired(message='请输入id')])


class AddCommentsForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容！')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id')])