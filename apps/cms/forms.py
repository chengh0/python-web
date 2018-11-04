#!/usr/bin/python
#  -*- coding: utf-8 -*-
from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,Length,InputRequired,EqualTo
from ..forms import BaseForm
from utils import clcache
from wtforms import ValidationError
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='密码格式输入错误')])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='密码格式输入错误')])
    newpwd = StringField(validators=[Length(6,20,message='密码格式输入错误')])
    newpwd1 = StringField(validators=[EqualTo("newpwd",message="两次密码输入不相同")])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱！')])
    captcha = StringField(validators=[Length(6,6,message='请输入正确长度的验证码！')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = clcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('修改邮箱不能与当前用户邮箱一致！')


class AddbannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入图片链接')])
    link_url = StringField(validators=[InputRequired(message='请输入图片跳转链接')])
    priority = IntegerField(validators=[InputRequired(message='请输入图片优先级')])


class UpdateBanner(AddbannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图id')])


class AddbordsForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称')])


class UboardsForm(AddbordsForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])
