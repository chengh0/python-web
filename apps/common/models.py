#!/usr/bin/python
#  -*- coding: utf-8 -*-
from exit import db
from datetime import datetime

class Boards(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)
    board_id = db.Column(db.Integer,db.ForeignKey('boards.id'))

    board = db.relationship('Boards',backref='posts')
    author = db.relationship('FrontUser',backref='front_posts')


class Essence_post(db.Model):
    __tablename__ = 'essence'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    create_time = db.Column(db.DateTime,default=datetime.now)

    post = db.relationship('PostModel',backref='essence')


class CommentsModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)

    post = db.relationship('PostModel',backref = 'comments')
    author = db.relationship('FrontUser',backref = 'comments')