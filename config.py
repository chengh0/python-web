#!/usr/bin/python
#  -*- coding: utf-8 -*-
import os


DEBUG = True

# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'yhgaduyasuhhdi'


ALLOWED_HOSTS = ['chengc.cc','129.28.17.88']

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'clbbs'
USERNAME = 'root'
PASSWORD = 'root'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False


CMS_USER_ID = 'BUDGHSIAHOLK'   #   user_id的变量
FRONT_USER_ID = 'byunjhouiwhqsn'

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = "69679502@qq.com"
MAIL_PASSWORD = "qtgtwarwhbofbgdd"
MAIL_DEFAULT_SENDER = "69679502@qq.com"


UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'apps/images') #用户上传的图片

PER_PAGE = 10 #帖子分页配置