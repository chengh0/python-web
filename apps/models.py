#!/usr/bin/python
#  -*- coding: utf-8 -*-
from exit import db
from datetime import datetime

class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    image_url = db.Column(db.String(255),nullable=False)
    link_url = db.Column(db.String(255),nullable=False)
    priority = db.Column(db.Integer,default=0)
    crate_time = db.Column(db.DateTime,default=datetime.now)


